"""Build identity, drift checks and explicit local installation. Python standard library only."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent
RECEIPT = '.oakheart-install.json'


def inventory(root):
    root = Path(root)
    if not root.exists():
        return {}
    result = {}
    for p in sorted(root.rglob('*')):
        if '__pycache__' in p.parts or p.suffix == '.pyc':
            continue
        if p.is_symlink():
            raise ValueError(f'Symlink not allowed: {p}')
        if p.is_file():
            result[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def input_digest():
    files = []
    for folder in ['source', 'adapters']:
        files += [(f'{folder}/{p}', h) for p, h in inventory(ROOT/folder).items()]
    for name in ['VERSION', 'source-manifest.json', 'build.py', 'validate.py', 'sync.py']:
        files.append((name, hashlib.sha256((ROOT/name).read_bytes()).hexdigest()))
    return hashlib.sha256(json.dumps(sorted(files), separators=(',', ':')).encode()).hexdigest()


def verify_release():
    receipt = json.loads((ROOT/'dist/release.json').read_text())
    assert receipt['input_sha256'] == input_digest(), 'Sources changed: rebuild first'
    assert receipt['version'] == (ROOT/'VERSION').read_text().strip(), 'Version mismatch'
    files = inventory(ROOT/'dist')
    files.pop('release.json')
    assert files == receipt['files'], 'Generated package changed: rebuild or preserve your edits as a proposal'
    return receipt


def refresh_manifest():
    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    names = {r['name']: r for r in manifest['skills']}
    manifest['skills'] = []
    for p in sorted((ROOT/'source').iterdir()):
        if not p.is_dir():
            raise ValueError(f'Unexpected source entry: {p}')
        assert re.fullmatch('[a-z0-9-]{1,64}', p.name) and (p/'SKILL.md').is_file(), p
        record = names.get(p.name, {'name': p.name})
        record['files'] = inventory(p)
        manifest['skills'].append(record)
    manifest['scope'] = 'Canonical shared sources; host-specific instructions are in adapters/. Evidence stays with the current task or authorized project.'
    (ROOT/'source-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')


def safe_target(target):
    target = Path(target).expanduser().absolute()
    for p in [target, *target.parents]:
        if p.is_symlink():
            raise ValueError(f'Refusing symlink destination: {p}')
    target = target.resolve()
    if target == ROOT or ROOT in target.parents or target in ROOT.parents:
        raise ValueError('Install into a separate destination, not this source checkout or its parents')
    if 'remote-skills' in target.parts:
        raise ValueError('Managed ChatGPT skills must be updated through Skill Creator')
    return target


def safe_unit(unit):
    if not re.fullmatch(r'[a-zA-Z0-9_.-]+', unit) or unit in ('.', '..', RECEIPT):
        raise ValueError(f'Invalid managed unit: {unit}')


def state(platform, target):
    release = verify_release()
    source = ROOT/'dist'/('codex/skills' if platform == 'codex' else 'oakheart')
    units = sorted(p.name for p in source.iterdir())
    record = target/RECEIPT
    previous = json.loads(record.read_text()) if record.exists() else None
    conflicts = []
    if previous:
        if previous['platform'] != platform:
            raise ValueError('Destination belongs to another platform')
        for unit, expected in previous['units'].items():
            safe_unit(unit)
            p = target/unit
            if p.is_symlink() or not p.is_dir() or inventory(p) != expected:
                conflicts.append(unit)
    for unit in units:
        safe_unit(unit)
        if (not previous or unit not in previous['units']) and (target/unit).exists():
            conflicts.append(unit)
    report = {'platform': platform, 'available_version': release['version'],
              'available_input_sha256': release['input_sha256'],
              'installed_version': previous['version'] if previous else None,
              'installed_input_sha256': previous['input_sha256'] if previous else None,
              'local_conflicts': sorted(set(conflicts)),
              'status': 'conflict' if conflicts else ('current' if previous and previous['input_sha256'] == release['input_sha256'] else 'update_available' if previous else 'not_installed'),
              'activation': 'not_verified'}
    return source, units, previous, report


def install(platform, target):
    target = safe_target(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock = target.parent / ('.oakheart-' + target.name + '.lock')
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as e:
        raise ValueError(f'Installation locked: {lock}. Confirm no installer is running before removing a stale lock.') from e
    os.close(fd)
    try:
        return _install(platform, target)
    finally:
        lock.unlink()


def _install(platform, target):
    source, units, previous, report = state(platform, target)
    if report['local_conflicts']:
        raise ValueError('Preserve and reconcile local edits before updating: '+', '.join(report['local_conflicts']))
    if report['status'] == 'current':
        return report
    target.mkdir(parents=True, exist_ok=True)
    all_units = sorted(set(units) | set(previous['units'] if previous else []))
    # Same filesystem staging, with rollback of all managed folders on failure.
    tmp = Path(tempfile.mkdtemp(prefix='.oakheart-stage-', dir=target.parent))
    cleanup = False
    try:
        for unit in units:
            shutil.copytree(source/unit, tmp/'new'/unit)
        new_record = {'platform': platform, 'version': report['available_version'],
                      'input_sha256': report['available_input_sha256'],
                      'units': {u: inventory(tmp/'new'/u) for u in units}}
        (tmp/'receipt').write_text(json.dumps(new_record, indent=2)+'\n')
        # Recheck after staging so edits made while copying are not overwritten.
        _, _, latest_previous, latest_report = state(platform, target)
        if latest_previous != previous or latest_report['local_conflicts']:
            shutil.rmtree(tmp)
            raise ValueError('Destination changed during staging; preserve and reconcile edits')
        moved, placed = [], []
        try:
            (tmp/'old').mkdir()
            for unit in all_units:
                p = target/unit
                if p.exists():
                    p.rename(tmp/'old'/unit)
                    moved.append(unit)
            for unit in moved:
                if not previous or unit not in previous['units'] or inventory(tmp/'old'/unit) != previous['units'][unit]:
                    raise ValueError('Destination changed during update; restoring original files')
            for unit in units:
                (tmp/'new'/unit).rename(target/unit)
                placed.append(unit)
            (tmp/'receipt').replace(target/RECEIPT)
            cleanup = True
        except BaseException:
            try:
                for unit in placed:
                    shutil.rmtree(target/unit)
                for unit in moved:
                    (tmp/'old'/unit).rename(target/unit)
                cleanup = True
            except BaseException as recovery_error:
                cleanup = False
                raise OSError(f'Update and rollback failed; preserved recovery files at {tmp}') from recovery_error
            raise
    finally:
        if cleanup:
            shutil.rmtree(tmp)
    return state(platform, target)[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('manifest', help='Refresh hashes after reviewing intentional source edits')
    sub.add_parser('verify', help='Check source and distribution hashes')
    for verb in ['status', 'install']:
        p = sub.add_parser(verb)
        p.add_argument('--platform', choices=['codex', 'code'], required=True)
        p.add_argument('--target', required=True, help='Codex skills directory or dedicated Claude plugin directory')
    args = parser.parse_args()
    try:
        if args.command == 'manifest':
            refresh_manifest()
        elif args.command == 'verify':
            r = verify_release()
            print(json.dumps({'version': r['version'], 'input_sha256': r['input_sha256'], 'verified': True}, indent=2))
        else:
            target = safe_target(args.target)
            result = install(args.platform, target) if args.command == 'install' else state(args.platform, target)[3]
            print(json.dumps(result, indent=2))
            if result['status'] == 'conflict':
                raise SystemExit(2)
    except (ValueError, AssertionError, KeyError, OSError) as e:
        parser.exit(2, f'{e}\n')


if __name__ == '__main__':
    main()
