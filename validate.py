"""Structural checks only: not native runtime or behavioral validation."""
from pathlib import Path
import ast
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent

def validate():
    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    verified = 0
    for record in manifest['skills']:
        source = ROOT/'source'/record['name']
        assert {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()} == set(record['files'])
        for rel, digest in record['files'].items():
            assert hashlib.sha256((ROOT/'source'/record['name']/rel).read_bytes()).hexdigest() == digest
            verified += 1
    skills = list((ROOT/'dist').glob('*/skills/*/SKILL.md')) + list((ROOT/'dist/chat-skills').glob('*/SKILL.md'))
    assert len(skills) == 3 * len(manifest['skills']), len(skills)
    links = 0
    for skill in skills:
        text = skill.read_text()
        assert text.startswith('---\n')
        header = text.split('---', 2)[1]
        name = re.search(r'^name: (.+)$', header, re.M)[1]
        assert name == skill.parent.name and re.fullmatch('[a-z0-9-]{1,64}', name)
        assert re.search(r'^description: .+', header, re.M)
        assert 'references/runtime.md' in text
        if 'codex' not in skill.parts:
            assert not list(skill.parent.rglob('openai.yaml'))
        for p in skill.parent.rglob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)', p.read_text()):
                if re.match(r'^[a-zA-Z]+:', link) or link.startswith('#'):
                    continue
                target = link.split('#')[0]
                assert (p.parent/target).exists(), f'Broken link: {p}: {target}'
                links += 1
        for script in skill.parent.rglob('*.py'):
            ast.parse(script.read_text())
    plugins = list((ROOT/'dist').glob('*/.claude-plugin/plugin.json'))
    assert len(plugins) == 1
    for p in plugins:
        data = json.loads(p.read_text())
        assert re.fullmatch('[a-z0-9-]+', data['name'])
        assert data['version'] == (ROOT/'VERSION').read_text().strip()
    # Organization sync and `claude plugin marketplace add` read this file.
    market = json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
    from vendor import verify as verify_vendor
    vendored = [e['name'] for e in verify_vendor()['plugins']]
    assert [e['name'] for e in market['plugins']] == [json.loads(p.read_text())['name'] for p in plugins] + vendored
    for entry in market['plugins']:
        assert entry['source'].startswith('./') and 'version' not in entry
        assert (ROOT/entry['source']/'.claude-plugin/plugin.json').is_file()
        assert not (ROOT/entry['source']/'bin').exists(), 'Organization sync rejects a top-level bin/'
    archives = list((ROOT/'dist/chat-uploads').rglob('*.zip'))
    assert len(archives) == len(manifest['skills'])
    for p in archives:
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None
            assert f'{p.stem}/SKILL.md' in z.namelist()
            assert all(n.startswith(p.stem+'/') and '..' not in Path(n).parts for n in z.namelist())
            tree = ROOT/'dist/chat-skills'/p.stem
            expected = {(Path(p.stem)/f.relative_to(tree)).as_posix():f.read_bytes() for f in tree.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
            assert set(z.namelist()) == set(expected), f'Archive inventory drift: {p}'
            assert all(z.read(name) == data for name,data in expected.items()), f'Archive content drift: {p}'
    from sync import verify_release
    verify_release()
    report = {'source_files_hash_verified':verified,'generated_skill_folders':len(skills),
              'relative_links_verified':links,'individual_upload_archives':len(archives),
              'plugin_manifests_json_checked':1,
              'vendored_plugins_hash_verified':len(vendored),
              'claude_cli_validation':'not_run_cli_unavailable',
              'claude_import_and_behavior':'not_tested',
              'real_project_parity':'pending_source_artifacts_and_claude_execution'}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    validate()
