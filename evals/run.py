"""Create a fresh frozen experiment and run paired answer-only tasks through Claude Code."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import random
import shutil
import subprocess
import tempfile
import uuid
from common import ROOT, files_digest, sha, write, invoke, verify_frozen


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',required=True,help='Explicit Claude model; actual observed identity is also recorded')
    p.add_argument('--tasks',type=Path,default=Path(__file__).with_name('tasks.json'))
    p.add_argument('--output-root',type=Path,required=True,help='Private output directory outside this repository')
    p.add_argument('--plugin',type=Path,default=ROOT/'dist/oakheart')
    p.add_argument('--baseline-plugin',type=Path,help='Optional prior-version plugin; otherwise baseline has no plugin')
    p.add_argument('--reps',type=int,default=2)
    p.add_argument('--seed',type=int,default=1)
    args=p.parse_args()
    if args.reps<1:p.error('--reps must be positive')
    outroot=args.output_root.expanduser().resolve()
    if outroot==ROOT or ROOT in outroot.parents:p.error('Store experiment outputs outside the reusable repository')
    cli=subprocess.check_output(['claude','--version'],text=True).strip()
    tasks=json.loads(args.tasks.read_text())
    ids=[t['id'] for t in tasks]
    if len(ids)!=len(set(ids)) or any(not i.replace('-','').replace('_','').isalnum() for i in ids):p.error('Task IDs must be unique safe identifiers')
    folder=outroot/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:12])
    folder.mkdir(parents=True,exist_ok=False)
    shutil.copytree(args.plugin,folder/'plugin')
    frozen={'plugin':files_digest(folder/'plugin')}
    if args.baseline_plugin:
        shutil.copytree(args.baseline_plugin,folder/'baseline-plugin');frozen['baseline-plugin']=files_digest(folder/'baseline-plugin')
    write(folder/'tasks.json',tasks);frozen['tasks.json']=sha((folder/'tasks.json').read_bytes())
    shutil.copytree(Path(__file__).parent,folder/'harness',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    frozen['harness']=files_digest(folder/'harness')
    harness=frozen['harness']
    jobs=[(t,c,n) for t in tasks for c in ['baseline','plugin','forced'] for n in range(args.reps) if c!='forced' or t.get('skill')]
    random.Random(args.seed).shuffle(jobs)
    write(folder/'manifest.json',{'schema':1,'created':datetime.now(timezone.utc).isoformat(),'requested_model':args.model,'cli_version':cli,'reps':args.reps,'seed':args.seed,'frozen':frozen,'harness_hashes':harness,'jobs':[(t['id'],c,n) for t,c,n in jobs],
      'scope':'Answer-only exploratory tasks; no browser, write or shell tools. Not native production or protected-holdout evidence. Managed host policies may still apply.'})
    print(folder,flush=True)
    for task,condition,rep in jobs:
        verify_frozen(folder)
        selected=(folder/'baseline-plugin' if args.baseline_plugin else None) if condition=='baseline' else folder/'plugin'
        prompt=task['prompt']+'\n\nReturn the requested answer directly. Do not create or edit files.'
        if condition=='forced':prompt='/oakheart:'+task['skill']+' '+prompt
        with tempfile.TemporaryDirectory(prefix='oakheart-case-') as cwd:
            result=invoke(prompt,args.model,cwd,selected)
        calls=[c for c in result['calls'] if c.get('name')=='Skill']
        expected='oakheart:'+str(task.get('skill'))
        result.update(task=task['id'],condition=condition,rep=rep,prompt_sha256=sha(prompt.encode()),
          invocation_requested=condition=='forced',skill_calls=calls,
          expected_skill_call_observed=any(isinstance(c.get('input'),dict) and c['input'].get('skill')==expected for c in calls),
          invocation_note='A slash-command request alone is not verified execution. Inspect raw events/read results; absence of a Skill event can be inconclusive for direct commands.')
        write(folder/'runs'/f'{task["id"]}__{condition}__{rep}.json',result)
        print(task['id'],condition,rep,'valid' if result['valid'] else 'blocked/invalid',flush=True)
    print('Use judge.py --experiment',folder,'--model <judge-model>',flush=True)

if __name__=='__main__':main()
