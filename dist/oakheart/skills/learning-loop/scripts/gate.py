#!/usr/bin/env python3
"""Read-only evidence consistency gate. A recommendation never authorizes a write."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REQUIRED = {'historical_failure', 'historical_success', 'variant', 'transfer', 'negative_control'}
SHA = re.compile(r'[0-9a-f]{64}')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def meaningful(value):
    return isinstance(value, str) and len(value.strip()) >= 12 and value.strip().lower() not in {'unknown', 'ambiguous', 'not applicable'}


def date(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.tzinfo is not None, 'timestamps must include timezone')
    return result


def load(path):
    return json.loads(Path(path).read_text())


def validate(path, current_baseline=None):
    """Verify local bytes and declared relationships, not authorship or causality."""
    errors = []
    try:
        e = load(path)
        root = Path(path).resolve().parent
        require(e['schema_version'] == 1, 'unsupported schema_version')
        artifacts = e['artifacts']
        require(isinstance(artifacts, dict) and artifacts, 'missing artifacts')
        resolved = {}
        for key, a in artifacts.items():
            p = (root / a['path']).resolve()
            require(p.is_relative_to(root) and p.is_file(), f'artifact missing or outside experiment: {key}')
            require(SHA.fullmatch(a['sha256']) is not None, f'invalid digest: {key}')
            require(hashlib.sha256(p.read_bytes()).hexdigest() == a['sha256'], f'artifact digest mismatch: {key}')
            require(p.stat().st_size > 0, f'empty artifact: {key}')
            resolved[key] = p

        def refs(values):
            require(isinstance(values, list) and values and all(x in artifacts for x in values), 'missing concrete artifact references')

        def evidence(record):
            require(meaningful(record['rationale']), 'missing concrete rationale')
            refs(record['evidence_refs'])

        protocol_ref = e['protocol_ref']
        refs([protocol_ref])
        p = load(resolved[protocol_ref])
        require(p['frozen'] is True, 'protocol not frozen')
        frozen = date(p['frozen_at'])
        require(frozen <= date(e['started_at']), 'protocol frozen after execution')
        require(e['thresholds'] == p['thresholds'], 'thresholds changed after freeze')
        limits = p['thresholds']
        require(all(type(limits[k]) is int and limits[k] >= 1 for k in ('target_wins', 'transfer_wins')), 'win thresholds must be at least one')
        for name in ('baseline', 'candidate'):
            ref = e[name + '_ref']
            refs([ref])
            require(artifacts[ref]['sha256'] == p[name + '_sha256'], f'{name} differs from frozen protocol')
        require(p['baseline_sha256'] != p['candidate_sha256'], 'candidate identical to baseline')
        if current_baseline is not None:
            require(current_baseline == p['baseline_sha256'], 'stale current baseline')
        for name in ('hypothesis', 'patch', 'dependencies', 'risks', 'rollback'):
            evidence(e[name])
        provenance = e['provenance']
        refs(provenance['evidence_refs'])
        require(meaningful(provenance['source']), 'missing provenance source')
        require(date(provenance['captured_at']) <= frozen, 'provenance postdates frozen protocol')
        require(e['creator_execution_id'].strip(), 'missing creator execution ID')
        require(e['diff_category'] == p['diff_category'], 'diff category changed after freeze')
        evidence(e['diff_attestation'])
        require(type(e['user_protected']) is bool and type(e['behavioral_change']) is bool, 'change classifications must be boolean')
        plan = p['cases']
        ids = [c['id'] for c in plan]
        require(ids and len(set(ids)) == len(ids), 'duplicate or missing planned case IDs')
        categories = {c['category'] for c in plan}
        require(REQUIRED <= categories, 'missing required case category')
        require(type(p['edge_required']) is bool, 'edge_required must be boolean')
        require(not p['edge_required'] or 'edge' in categories, 'missing required edge case')
        require(meaningful(p['edge_rationale']), 'missing edge-case applicability rationale')
        runs = e['cases']
        require(len(runs) == len(ids) and {c['id'] for c in runs} == set(ids), 'case coverage differs from frozen protocol')
        generators = {c[v]['execution_id'] for c in runs for v in ('baseline', 'candidate')}
        judges = {c['judge']['execution_id'] for c in runs}
        require(e['creator_execution_id'] not in generators, 'editor and generator roles overlap')
        require(not judges & (generators | {e['creator_execution_id']}), 'judge and generator/editor roles overlap across experiment')
        wins = {'target': 0, 'transfer': 0}
        for spec in plan:
            c = next(c for c in runs if c['id'] == spec['id'])
            require(spec['category'] in REQUIRED | {'edge'}, 'unknown case category')
            require(spec['bucket'] in {'target', 'transfer', 'guard'}, 'unknown case bucket')
            require((spec['category'] == 'transfer') == (spec['bucket'] == 'transfer'), 'transfer bucket/category mismatch')
            require(spec['category'] not in {'historical_success', 'negative_control'} or spec['bucket'] == 'guard', 'control cases cannot count as target wins')
            refs([spec['input_ref']])
            require(isinstance(spec['conditions'], dict) and all(k in spec['conditions'] for k in ('model', 'tools', 'budget', 'environment')), 'missing matched-run conditions')
            require(isinstance(spec['conditions']['model'], str) and spec['conditions']['model'].strip().lower() not in {'', 'unknown', 'ambiguous'}, 'model provenance unknown; exploratory evidence only')
            outputs = []
            for version in ('baseline', 'candidate'):
                run = c[version]
                refs([run['output_ref']])
                outputs.append(run['output_ref'])
                require(run['full_output'] is True, 'partial paired output')
                require(run['conditions'] == spec['conditions'], 'unmatched run conditions')
                require(date(run['started_at']) >= date(e['started_at']), 'run predates experiment')
                require(run['execution_id'].strip(), 'missing run execution ID')
            require(c['baseline']['execution_id'] != c['candidate']['execution_id'], 'paired executions must differ')
            require(c['candidate']['objective_pass'] is True, 'candidate objective failure or unknown')
            require(c['candidate']['critical_failures'] == [], 'candidate critical failure or unknown')
            j = c['judge']
            require(j['execution_id'].strip() and j['execution_id'] not in {e['creator_execution_id'], c['baseline']['execution_id'], c['candidate']['execution_id']}, 'judge execution is not independent')
            labels = spec['label_to_version']
            require(set(labels) == {'A', 'B'} and set(labels.values()) == {'baseline', 'candidate'}, 'invalid blind label mapping')
            require(sorted(spec['presentation_order']) == ['A', 'B'] and j['presentation_order'] == spec['presentation_order'], 'blind presentation order mismatch')
            require(j['seen_labels'] == ['A', 'B'] and j['identity_hidden'] is True, 'judge was not blinded')
            refs([j['raw_ref']])
            evidence(j)
            require(set(outputs) <= set(j['evidence_refs']), 'judgment must reference both full outputs')
            require(j['outcome'] in {'win', 'tie', 'loss'}, 'unknown or ambiguous case outcome')
            require(j['regression'] == 'none' and j['outcome'] != 'loss', 'regression or loss requires hold')
            if j['outcome'] == 'win' and spec['bucket'] in wins:
                wins[spec['bucket']] += 1
        require(wins['target'] >= limits['target_wins'] and wins['transfer'] >= limits['transfer_wins'], 'insufficient target/transfer wins; ties do not count')
        automatic = (not e['user_protected'] and not e['behavioral_change'] and e['diff_category'] in {'nonbehavioral_reference_addition', 'test_addition'})
        return {'status': 'eligible_for_human_review' if automatic else 'eligible_requires_approval', 'wins': wins, 'authorization': False, 'release_ready': False, 'pending_release_gates': ['human_calibration', 'blind_human_preference_labels', 'access_separated_holdout', 'fresh_session_activation'], 'limitation': 'Hashes and execution IDs cannot authenticate self-attested provenance, independence, blinding, or diff classification.'}
    except (KeyError, ValueError, TypeError, OSError, AttributeError, StopIteration) as exc:
        errors.append(str(exc))
    return {'status': 'hold', 'reasons': errors, 'authorization': False, 'release_ready': False}


def monitor(path):
    """Count observed opportunities by correction, skill, task class and version."""
    try:
        data = load(path)
        promotions = data.get('promotions', [])
        for p in promotions:
            date(p['promoted_at'])
            require(all(isinstance(p[k], str) and p[k].strip() and p[k] != 'unknown' for k in ('correction_id', 'skill', 'version_id')), 'promotion needs correction, skill and known version')
        seen, groups, reopened, pending = {}, {}, [], []
        aggregate = {'eligible_observed_opportunities': 0, 'corrections': 0, 'successes': 0, 'unknown': 0}
        for o in data['observations']:
            oid = o['observation_id']
            require(isinstance(oid, str) and oid.strip(), 'missing observation ID')
            if oid in seen:
                require(seen[oid] == o, 'conflicting duplicate observation ID')
                continue
            seen[oid] = o
            at = date(o['observed_at'])
            require(type(o['eligible']) is bool and type(o['observed']) is bool, 'eligibility/observation must be boolean')
            require(o['result'] in {'success', 'correction', 'unknown'}, 'invalid observation result')
            require(all(isinstance(o[k], str) and o[k].strip() for k in ('correction_id', 'skill', 'task_class')), 'missing correction, skill or task class')
            version = o.get('version_id') or 'unknown'
            require(isinstance(version, str), 'version must be a string')
            key = (o['correction_id'], o['skill'], o['task_class'], version)
            c = groups.setdefault(key, dict(eligible_observed_opportunities=0, corrections=0, successes=0, unknown=0, correction_id=key[0], skill=key[1], task_class=key[2], version_id=key[3]))
            # New groups start at zero, never inherit accumulated aggregate counts.
            if not (o['eligible'] and o['observed']):
                continue
            require(meaningful(o['evidence']), 'missing observation evidence')
            field = {'success': 'successes', 'correction': 'corrections', 'unknown': 'unknown'}[o['result']]
            for counts in (c, aggregate):
                counts['eligible_observed_opportunities'] += 1
                counts[field] += 1
            relevant = [p for p in promotions if p['correction_id'] == key[0] and p['skill'] == key[1] and date(p['promoted_at']) < at]
            if o['result'] == 'correction' and relevant:
                promotion = max(relevant, key=lambda p: date(p['promoted_at']))
                event = {'observation_id': oid, 'correction_id': key[0], 'skill': key[1], 'task_class': key[2], 'observed_version': version, 'promoted_version': promotion['version_id']}
                reopened.append(event)
                if version != promotion['version_id']:
                    pending.append(event)
        for c in [aggregate, *groups.values()]:
            n = c['eligible_observed_opportunities']
            confirmed = c['corrections'] + c['successes']
            c['observed_correction_rate_lower_bound'] = c['corrections'] / n if n else None
            c['confirmed_outcomes_correction_rate'] = c['corrections'] / confirmed if confirmed else None
        return {'status': 'attribution_pending' if pending else ('reopen' if reopened else 'observed'), 'counts': list(groups.values()), 'aggregate': aggregate, 'reopened': reopened, 'attribution_pending': pending, 'authorization': False, 'release_ready': False}
    except (KeyError, ValueError, TypeError, OSError, AttributeError) as exc:
        return {'status': 'hold', 'reasons': [str(exc)], 'authorization': False, 'release_ready': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    v = sub.add_parser('validate')
    v.add_argument('experiment')
    v.add_argument('--current-baseline-sha256', help='digest of current live skill snapshot; omit only for offline review')
    m = sub.add_parser('monitor')
    m.add_argument('observations')
    args = parser.parse_args()
    result = validate(args.experiment, args.current_baseline_sha256) if args.command == 'validate' else monitor(args.observations)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result['status'] == 'hold' else 0


if __name__ == '__main__':
    sys.exit(main())
