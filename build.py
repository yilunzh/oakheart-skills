"""Build platform distributions from the canonical shared source. Stdlib only."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
ADAPTER = ROOT / 'adapters'

MODES = {'chat': 'chat-skills', 'code': 'oakheart/skills', 'codex': 'codex/skills'}
COMMON = (ADAPTER / 'common.md').read_text()
VERSION = (ROOT / 'VERSION').read_text().strip()


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

def zipped(directory, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(directory.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                info = zipfile.ZipInfo((Path(directory.name) / p.relative_to(directory)).as_posix(), (2026, 9, 26, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, p.read_bytes())

def build():
    dist = ROOT / '.dist-build'
    if dist.exists():
        shutil.rmtree(dist)
    manifest = json.loads((ROOT / 'source-manifest.json').read_text())
    names = [record['name'] for record in manifest['skills']]
    assert len(names) == len(set(names)), 'Duplicate skill names'
    assert set(names) == {p.name for p in (ROOT/'source').iterdir()}, 'Source inventory changed: refresh manifest after review'
    patches = []
    for record in manifest['skills']:
        name = record['name']
        source = ROOT / 'source' / name
        actual = {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()}
        assert actual == set(record['files']), f'Source file inventory drift: {name}'
        assert not any(p.is_symlink() for p in source.rglob('*')), f'Source symlink: {name}'
        for rel, expected in record['files'].items():
            assert hashlib.sha256((source / rel).read_bytes()).hexdigest() == expected, f'Source drift: {name}/{rel}'
        for mode in MODES:
            plugin = 'oakheart'
            dest = dist / MODES[mode] / name
            ignored = ['__pycache__', '*.pyc'] + ([] if mode == 'codex' else ['openai.yaml'])
            shutil.copytree(source, dest, ignore=shutil.ignore_patterns(*ignored))
            p = dest / 'SKILL.md'
            text = p.read_text()
            marker = text.find('\n---', 4) + 4
            text = text[:marker] + '\n\nUse available host capabilities and relative reference paths. Read [runtime guidance](references/runtime.md) only when resolving a tool dependency, independent review, installation or skill maintenance; do not narrate routine setup.\n' + text[marker:]
            p.write_text(text)
            write(dest / 'references/runtime.md', COMMON + (ADAPTER / (mode + '.md')).read_text())
            paths = {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()} | {p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file()}
            for rel in sorted(paths):
                a, b = source/rel, dest/rel
                before_bytes = a.read_bytes() if a.exists() else b''
                after_bytes = b.read_bytes() if b.exists() else b''
                if before_bytes == after_bytes:
                    continue
                before_text, after_text = before_bytes.decode('utf-8'), after_bytes.decode('utf-8')
                patches.extend(difflib.unified_diff(before_text.splitlines(True), after_text.splitlines(True), fromfile='source/'+name+'/'+rel, tofile=mode+'/'+name+'/'+rel))
            if mode == 'chat':
                group = 'main'
                zipped(dest, dist / 'chat-uploads' / group / (name + '.zip'))
    for plugin in ['oakheart']:
        write(dist/plugin/'.claude-plugin/plugin.json', json.dumps({
            'name':plugin, 'version':VERSION, 'description':'Shared Oakheart skills; native activation and behavioral parity require verification.',
            'author':{'name':'Yilun Zhang'}}, indent=2)+'\n')
        shutil.copytree(ADAPTER/'agents', dist/plugin/'agents')
        for added in [dist/plugin/'.claude-plugin/plugin.json', dist/plugin/'agents/artifact-reviewer.md']:
            patches.extend(difflib.unified_diff([], added.read_text().splitlines(True), fromfile='/dev/null', tofile=added.relative_to(dist).as_posix()))
    write(dist/'adaptation.diff', ''.join(patches))
    from sync import input_digest, inventory
    receipt = {'version': VERSION, 'input_sha256': input_digest(),
               'targets': MODES, 'files': inventory(dist)}
    write(dist/'release.json', json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    target = ROOT/'dist'
    previous = ROOT/'.dist-previous'
    if previous.exists():
        shutil.rmtree(previous)
    if target.exists():
        target.rename(previous)
    try:
        dist.rename(target)
    except Exception:
        if previous.exists():
            previous.rename(target)
        raise
    if previous.exists():
        shutil.rmtree(previous)
    print(f'Built {len(manifest["skills"])} skills for Claude chat, Claude Code and Codex ({VERSION}).')

if __name__ == '__main__':
    build()
