"""Record or verify pinned third-party plugins in vendor/. Python standard library only.

Vendored plugins are provider-owned: they are copied unmodified from a reviewed
upstream commit, never rewritten by build.py, and listed in the marketplace beside
the oakheart plugin. `record` is bookkeeping after a reviewed update, not approval.
"""
from pathlib import Path
import argparse
import json
import re
from sync import inventory

ROOT = Path(__file__).resolve().parent
VENDOR = ROOT/'vendor'
MANIFEST = VENDOR/'manifest.json'


def load():
    return json.loads(MANIFEST.read_text())


def plugin_name(folder):
    return json.loads((folder/'.claude-plugin/plugin.json').read_text())['name']


def record(name, commit):
    assert re.fullmatch('[0-9a-f]{40}', commit), 'Record the full upstream commit hash'
    manifest = load()
    entry = next(e for e in manifest['plugins'] if e['name'] == name)
    folder = VENDOR/name
    entry['commit'] = commit
    entry['version'] = json.loads((folder/'.claude-plugin/plugin.json').read_text())['version']
    entry['files'] = inventory(folder)
    MANIFEST.write_text(json.dumps(manifest, indent=2)+'\n')


def verify():
    manifest = load()
    folders = sorted(p.name for p in VENDOR.iterdir() if p.is_dir())
    assert folders == sorted(e['name'] for e in manifest['plugins']), 'Vendor inventory changed: record it after review'
    for entry in manifest['plugins']:
        folder = VENDOR/entry['name']
        assert plugin_name(folder) == entry['name'], f'Plugin name differs from folder: {folder}'
        assert re.fullmatch('[0-9a-f]{40}', entry['commit']) and entry['license'], entry['name']
        assert not (folder/'bin').exists(), 'Organization sync rejects a top-level bin/'
        assert inventory(folder) == entry['files'], f'Vendored files differ from the recorded upstream copy: {folder}'
        version = json.loads((folder/'.claude-plugin/plugin.json').read_text())['version']
        assert version == entry['version'], f'Vendored version mismatch: {folder}'
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    rec = sub.add_parser('record')
    rec.add_argument('name')
    rec.add_argument('commit')
    sub.add_parser('verify')
    args = parser.parse_args()
    if args.command == 'record':
        record(args.name, args.commit)
    verify()
    print('Vendored plugins verified.')
