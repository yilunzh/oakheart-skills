"""Build Claude distributions from the preserved personal-skill snapshot. Stdlib only."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
ADAPTER = ROOT / 'adapters'

REPLACEMENTS = {
    'learning-loop/SKILL.md': [
        ('Keep ChatGPT as the runtime. Use existing task skills and Skill Creator; do not install an external agent, require API billing, or rewrite provider instructions.',
         'Use the current authorized Claude environment and existing task skills. Use the skill-maintenance procedure in references/runtime.md for changes to these exported personal skills; do not require API billing or rewrite provider instructions.'),
        ('use Skill Creator for authorized updates', 'use the skill-maintenance procedure in references/runtime.md for authorized updates'),
    ],
    'learning-loop/references/operations.md': [
        ('The personal-skills checkout managed through Skill Creator is the source of truth for installed instructions.',
         'The owner-designated version-controlled source is the source of truth for these exported personal instructions; generated Claude packages are distribution copies.'),
        ('using Skill Creator', 'using the skill-maintenance procedure in runtime.md'),
        ('through Skill Creator', 'using the skill-maintenance procedure in runtime.md'),
    ],
    'learning-loop/references/learning.md': [
        ('through the connected GitHub app', 'through an authorized GitHub connection or an existing checkout of that branch'),
        ('Do not create a parallel Library ledger. Use Skill Creator for installed instructions. Keep repository-backed experiment records there; use Library only for requested standalone reports.',
         'Do not create a parallel evidence ledger. Use the skill-maintenance procedure in runtime.md for these exported instructions. Keep repository-backed experiment records there; save standalone reports to the user-designated durable destination.'),
    ],
    'software-delivery-agency/references/operating.md': [
        ('Save runtime records and deliverables through Library unless they belong to an existing externally synced project.',
         'Save runtime records and deliverables to the user-designated project or durable connected storage. For existing repository-backed projects, keep their established destination. A temporary sandbox file is not evidence of durable saving.'),
    ],
    'software-delivery-agency/references/engineering-release.md': [
        ('use Sites for Sites projects',
         'preserve the established hosting and release workflow; an existing ChatGPT Sites project requires its authorized Sites environment unless migration is explicitly requested'),
    ],
    'software-delivery-agency/SKILL.md': [
        ('Sites Building/Hosting for Sites projects; existing project workflow otherwise',
         'Existing project build/hosting workflow; see references/runtime.md for ChatGPT Sites limitations'),
        ('Skill Creator; independent task execution', 'Version-controlled skill maintenance; independent task execution'),
    ],
}

COMMON = """# Runtime and dependency adaptation

This is a portability adaptation of a personal skill snapshot, not proof of equivalent Claude behavior. Follow the host's tool, permission, and instruction rules. Historical test results in bundled references describe the source workflow, not tests performed in Claude.

Read supporting paths relative to this skill's directory. Run bundled scripts from that directory, with Python 3, after inspecting their inputs. The family-crest inspector additionally needs Pillow. Never interpret OpenAI UI metadata as Claude configuration.

Resolve companion skills by their frontmatter name among installed skills; plugin names may be namespaced. Load each needed companion once and avoid circular handoffs. The main pack includes copy-reviewer, sales-pitch-reviewer, business-strategy-copilot, software-delivery-agency, and learning-loop. Family-crest-studio is an optional separate candidate package.

## Capability mapping

- **Sales:** The source Sales plugin is not bundled. Use an installed equivalent when available. Otherwise use the bundled pitch-review criteria and supplied evidence for bounded commercial drafting/review, and disclose missing Sales-specific research or account checks. Do not claim the original Sales workflow ran or fabricate CRM data.
- **Artifact production:** Discover the host's document, presentation, spreadsheet, PDF, browser, and image tools when needed. Use actual rendering and behavioral inspection when required. If a required capability is absent, complete supported work and identify the precise missing validation. Text review is not visual QA.
- **Sites:** No ChatGPT Sites credentials, project tools, or hosting are transferred. Use the existing project's actual repository/build/release workflow. An existing Sites deployment must be handled in its authorized environment until migration is explicitly requested. Do not create a replacement deployment implicitly.
- **Library and context:** ChatGPT Library, memories, previous chats, and project files do not transfer with a skill. Use supplied artifacts and authorized connected storage. Ask for a missing authoritative artifact only when it controls the task. Never invent prior decisions.
- **Scheduling:** Importing skills creates no recurring jobs. Existing ChatGPT automations stay separate. Scheduling in Claude requires an available scheduler and a verified creation result; do not create duplicate jobs merely to mirror this pack.
- **Images:** Family-crest visual creation and editing require an available image-generation/editing capability. A prompt, SVG sketch, or text description is not a completed faithful image edit.

## Skill maintenance

For an authorized change, read the current source, relevant evidence, dependencies, and existing promotion policy. Preserve an exact baseline and a bounded diff. Edit the owner-designated source and adapter files, not only generated ZIPs or installed plugin caches. Run relevant checks, rebuild distributions, record the version and content hashes, and save through the established version-control workflow. Keep unapproved candidates outside installed skill paths. Only report activation after checking the installed version in a fresh session.

Preserve the existing learning ledger at `yilunzh/personal-os`, branch `feature/skill-learning-loop`, paths `learning-loop/WORKFLOW.md` and `learning-loop/state.json`. It is not bundled or connected by this export. Read its current policy before maintenance; do not rewrite it to relax release gates. If unavailable, report the missing ledger access; a local proposal is not a recorded promotion. A Claude migration does not approve future behavioral changes or overwrite the ChatGPT originals.
"""

MODES = {
    'chat': """\n## Claude chat and Cowork execution

Use enabled skills and capabilities actually present in the current session. Uploading a skill does not provision subagents, connectors, credentials, or shell packages. When the host cannot start a genuinely separate reviewer execution, label the review as self-review only. A role-play pass in the same context is not independent. Hold learning-loop promotions that require independent execution; ordinary authorized drafting can still proceed with a stated review limitation.
""",
    'code': """\n## Claude Code execution

When a skill calls for independent editorial review, delegate a fresh execution to the plugin's `artifact-reviewer` (namespaced `oakheart:artifact-reviewer` in the main plugin). Provide only the task brief, permitted changes, relevant source evidence, artifact paths, and applicable rubric. Do not include creator self-ratings, expected verdicts, or target scores. The reviewer returns findings; the creator makes edits. A reviewer must not spawn another reviewer.

The reviewer is limited to reading files and cannot run a browser, render files, or execute tests. Provide actual visual/behavioral evidence separately or use a separately authorized QA execution; never claim these checks from text inspection. Read-only tools do not enforce filesystem isolation: a separate reviewer context is not an access-separated holdout. Learning-loop release gates still require their stated evidence and isolation.
""",
}

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
            plugin = 'oakheart-optional-crest' if record['export_group'] == 'optional' else 'oakheart'
            dest = dist / ('chat-skills' if mode == 'chat' else plugin + '/skills') / name
            shutil.copytree(source, dest, ignore=shutil.ignore_patterns('openai.yaml', '__pycache__', '*.pyc'))
            for relkey, pairs in REPLACEMENTS.items():
                if not relkey.startswith(name + '/'):
                    continue
                rel = relkey[len(name)+1:]
                p = dest / rel
                before = p.read_text()
                after = before
                for old, new in pairs:
                    assert old in after, f'Missing adapter anchor: {relkey}: {old}'
                    after = after.replace(old, new)
                p.write_text(after)
            p = dest / 'SKILL.md'
            text = p.read_text()
            marker = text.find('\n---', 4) + 4
            text = text[:marker] + '\n\nBefore applying this workflow, read [runtime and dependency adaptation](references/runtime.md).\n' + text[marker:]
            p.write_text(text)
            write(dest / 'references/runtime.md', COMMON + MODES[mode].replace('`oakheart:artifact-reviewer`', '`'+plugin+':artifact-reviewer`'))
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
                group = 'optional' if record['export_group'] == 'optional' else 'main'
                zipped(dest, dist / 'chat-uploads' / group / (name + '.zip'))
    for plugin in ['oakheart', 'oakheart-optional-crest']:
        write(dist/plugin/'.claude-plugin/plugin.json', json.dumps({
            'name':plugin, 'version':'0.1.0', 'description':'Personal skills portability preview; Claude runtime validation pending.',
            'author':{'name':'Yilun Zhang'}}, indent=2)+'\n')
        shutil.copytree(ADAPTER/'agents', dist/plugin/'agents')
        for added in [dist/plugin/'.claude-plugin/plugin.json', dist/plugin/'agents/artifact-reviewer.md']:
            patches.extend(difflib.unified_diff([], added.read_text().splitlines(True), fromfile='/dev/null', tofile=added.relative_to(dist).as_posix()))
    write(dist/'adaptation.diff', ''.join(patches))
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
    print('Built five main skills and one optional candidate for chat and Code.')

if __name__ == '__main__':
    build()
