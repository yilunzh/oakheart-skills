"""Summarize all expected answer pairs, preserving blocked and missing judgments."""
import argparse
from collections import Counter
import json
from pathlib import Path
from common import combine_orders, sha, verify_frozen, files_digest


def summarize(experiment_manifest, records):
    result={}
    pairs=[(task,cond,rep) for task,cond,rep in experiment_manifest['jobs'] if cond!='baseline']
    expected={(task,cond,rep,order) for task,cond,rep in pairs for order in ['AB','BA']}
    if set(records)-expected:raise ValueError('Unexpected judgment keys')
    for task,cond,rep in pairs:
        counts=result.setdefault(cond,Counter())
        counts['expected_pairs']+=1
        js=[records.get((task,cond,rep,o)) for o in ['AB','BA']]
        if any(j is None for j in js):counts['missing_pairs']+=1;continue
        if any(j['status']!='graded' for j in js):counts['blocked_or_invalid_pairs']+=1;continue
        counts['complete_pairs']+=1;counts[combine_orders(js)]+=1
        for side in ['candidate','baseline']:
            if any(j[side]['critical_fail'] for j in js):counts[side+'_critical_pairs']+=1
            if any(j[side]['unsupported_claims'] for j in js):counts[side+'_unsupported_pairs']+=1
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--batch',type=Path,required=True);args=p.parse_args()
    batch=args.batch.resolve();exp=batch.parent.parent;em=verify_frozen(exp)
    m=json.loads((batch/'manifest.json').read_text())
    assert m['experiment_manifest_sha256']==sha((exp/'manifest.json').read_bytes()),'Manifest changed'
    assert files_digest(batch/'harness')==m['harness_hashes'],'Judging implementation snapshot changed'
    for name,digest in m['runs'].items():assert sha((exp/'runs'/name).read_bytes())==digest,'Run changed after judging'
    records={}
    for f in batch.glob('*.json'):
        if f.name=='manifest.json':continue
        j=json.loads(f.read_text());key=(j['task'],j['condition'],j['rep'],j['order'])
        if key in records:raise ValueError('Duplicate judgment')
        records[key]=j
    counts=summarize(em,records)
    print(json.dumps({'task_prompts':len(json.loads((exp/'tasks.json').read_text())),
      'analysis_sha256':sha(Path(__file__).read_bytes()),'common_sha256':sha(Path(__file__).with_name('common.py').read_bytes()),
      'pair_counts_by_condition':counts,
      'interpretation':'Each pair combines two presentation orders. Disagreement is order_sensitive, not an extra win. Repeats and reused baselines are correlated. Missing and invalid executions remain in denominators. Confirm skill execution from traces; forced requests alone do not establish invocation. Model grades require human calibration; no significance or promotion claim.'},indent=2))

if __name__=='__main__':main()
