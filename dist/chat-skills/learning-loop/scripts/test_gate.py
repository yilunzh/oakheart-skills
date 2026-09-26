"""Run: python -m unittest discover -s scripts -p 'test_gate.py' -v"""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import gate


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.e = {'schema_version': 1, 'artifacts': {}, 'protocol_ref': 'protocol',
                  'baseline_ref': 'baseline', 'candidate_ref': 'candidate',
                  'started_at': '2026-09-20T12:00:00Z', 'creator_execution_id': 'creator-1',
                  'thresholds': {'target_wins': 1, 'transfer_wins': 1},
                  'diff_category': 'behavioral_change', 'user_protected': True,
                  'behavioral_change': True, 'cases': []}
        for key in ['baseline', 'candidate', 'source', 'patch']:
            self.artifact(key, f'Full raw {key} content, independently inspectable.')
        for key in ['hypothesis', 'patch', 'dependencies', 'risks', 'rollback', 'diff_attestation']:
            self.e[key] = {'rationale': f'Concrete {key}: inspect artifact for exact mechanism and scope.', 'evidence_refs': ['patch']}
        self.e['provenance'] = {'source': 'User correction in dated source transcript.', 'captured_at': '2026-09-19T12:00:00Z', 'evidence_refs': ['source']}
        self.p = {'frozen': True, 'frozen_at': '2026-09-20T11:00:00Z',
                  'baseline_sha256': self.e['artifacts']['baseline']['sha256'],
                  'candidate_sha256': self.e['artifacts']['candidate']['sha256'],
                  'thresholds': dict(self.e['thresholds']), 'diff_category': self.e['diff_category'],
                  'edge_required': False, 'edge_rationale': 'No separate boundary behavior touched by this change.', 'cases': []}
        for i, category in enumerate(sorted(gate.REQUIRED)):
            case_id = f'case-{i}'
            conditions = {'model': 'pinned-model-version', 'tools': [], 'budget': 2000, 'environment': 'snapshot-1'}
            self.artifact(case_id + '-input', 'Original full case input and exact expected behavior.')
            self.p['cases'].append({'id': case_id, 'category': category,
                                    'bucket': 'transfer' if category == 'transfer' else ('target' if category == 'historical_failure' else 'guard'),
                                    'input_ref': case_id + '-input', 'conditions': conditions,
                                    'label_to_version': {'A': 'candidate', 'B': 'baseline'}, 'presentation_order': ['B', 'A']})
            c = {'id': case_id}
            for version in ['baseline', 'candidate']:
                ref = case_id + '-' + version
                self.artifact(ref, f'Complete {version} output for {case_id}.')
                c[version] = {'output_ref': ref, 'full_output': True, 'conditions': dict(conditions), 'started_at': self.e['started_at'], 'execution_id': ref, 'objective_pass': True, 'critical_failures': []}
            self.artifact(case_id + '-judge', 'Raw blinded judgment with concrete quotations and comparison.')
            c['judge'] = {'execution_id': case_id + '-judge', 'presentation_order': ['B', 'A'], 'seen_labels': ['A', 'B'],
                          'identity_hidden': True, 'raw_ref': case_id + '-judge', 'rationale': 'Candidate resolves exact failure documented in output artifacts.',
                          'evidence_refs': [case_id + '-baseline', case_id + '-candidate'],
                          'outcome': 'win' if category in ['historical_failure', 'transfer'] else 'tie', 'regression': 'none'}
            self.e['cases'].append(c)
        self.freeze()

    def artifact(self, key, content):
        (self.root / (key + '.txt')).write_text(content)
        self.e['artifacts'][key] = {'path': key + '.txt', 'sha256': hashlib.sha256(content.encode()).hexdigest()}

    def freeze(self):
        self.artifact('protocol', json.dumps(self.p, sort_keys=True))

    def result(self, current=None):
        path = self.root / 'experiment.json'
        path.write_text(json.dumps(self.e))
        return gate.validate(path, current)

    def hold(self):
        self.assertEqual(self.result()['status'], 'hold')

    def test_pass_still_requires_user_approval(self):
        result = self.result(self.p['baseline_sha256'])
        self.assertEqual(result['status'], 'eligible_requires_approval')
        self.assertFalse(result['authorization'])
        self.assertFalse(result['release_ready'])

    def test_nonbehavioral_eligibility_is_not_authorization(self):
        self.e.update(user_protected=False, behavioral_change=False, diff_category='test_addition')
        self.p['diff_category'] = 'test_addition'
        self.freeze()
        self.assertEqual(self.result()['status'], 'eligible_for_human_review')
        self.assertFalse(self.result()['authorization'])

    def test_missing_required_case(self):
        self.p['cases'] = [c for c in self.p['cases'] if c['category'] != 'negative_control']
        self.freeze()
        self.hold()

    def test_missing_raw_artifact(self):
        (self.root / 'source.txt').unlink()
        self.hold()

    def test_fake_digest(self):
        self.e['artifacts']['source']['sha256'] = 'fabricated'
        self.hold()

    def test_wrong_hash(self):
        (self.root / 'source.txt').write_text('tampered output')
        self.hold()

    def test_missing_pair(self):
        del self.e['cases'][0]['candidate']
        self.hold()

    def test_fake_independence(self):
        self.e['cases'][0]['judge']['execution_id'] = 'creator-1'
        self.hold()

    def test_thresholds_changed(self):
        self.e['thresholds']['target_wins'] = 0
        self.hold()

    def test_regression(self):
        self.e['cases'][0]['judge']['regression'] = 'material'
        self.hold()

    def test_ties_only(self):
        for c in self.e['cases']:
            c['judge']['outcome'] = 'tie'
        self.hold()

    def test_stale_current_baseline(self):
        self.assertEqual(self.result('0' * 64)['status'], 'hold')

    def test_unknown_outcome(self):
        self.e['cases'][0]['judge']['outcome'] = 'unknown'
        self.hold()

    def test_conditions_changed(self):
        self.e['cases'][0]['candidate']['conditions']['budget'] = 3000
        self.hold()

    def test_blind_order_changed(self):
        self.e['cases'][0]['judge']['presentation_order'] = ['A', 'B']
        self.hold()

    def test_read_only(self):
        self.result()
        before = {p: p.read_bytes() for p in self.root.iterdir()}
        gate.validate(self.root / 'experiment.json')
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.iterdir()})

    def test_monitor_recurrence_dedup_unknown(self):
        o = {'observation_id': 'obs-1', 'correction_id': 'correction-1', 'skill': 'skill-a', 'task_class': 'edit', 'eligible': True, 'observed': True,
             'result': 'correction', 'version_id': 'version-2', 'observed_at': '2026-09-22T12:00:00Z', 'evidence': 'Same corrected behavior recurred in captured transcript.'}
        unknown = dict(o, observation_id='obs-2', result='unknown')
        ignored = dict(o, observation_id='obs-3', observed=False)
        data = {'promotions': [{'correction_id': 'correction-1', 'skill': 'skill-a', 'version_id': 'version-2', 'promoted_at': '2026-09-21T12:00:00Z'}], 'observations': [o, copy.deepcopy(o), unknown, ignored]}
        path = self.root / 'observations.json'
        path.write_text(json.dumps(data))
        result = gate.monitor(path)
        self.assertEqual(result['status'], 'reopen')
        self.assertEqual(result['reopened'][0]['correction_id'], 'correction-1')
        self.assertEqual(result['aggregate'], {'eligible_observed_opportunities': 2, 'corrections': 1, 'successes': 0, 'unknown': 1, 'observed_correction_rate_lower_bound': 0.5, 'confirmed_outcomes_correction_rate': 1.0})

    def test_unknown_version_reopens_without_blame(self):
        path = self.root / 'observations.json'
        path.write_text(json.dumps({'promotions': [{'correction_id': 'c1', 'skill': 'skill-a', 'version_id': 'v2', 'promoted_at': '2026-09-21T12:00:00Z'}], 'observations': [{'observation_id': 'o1', 'correction_id': 'c1', 'skill': 'skill-a', 'task_class': 'edit', 'eligible': True, 'observed': True, 'result': 'correction', 'version_id': 'unknown', 'observed_at': '2026-09-22T12:00:00Z', 'evidence': 'Observed recurrence with activation version unavailable.'}]}))
        result = gate.monitor(path)
        self.assertEqual(result['status'], 'attribution_pending')
        self.assertEqual(result['reopened'][0]['correction_id'], 'c1')
        self.assertEqual(result['attribution_pending'][0]['correction_id'], 'c1')

    def test_candidate_objective_failure_and_unknown_hold(self):
        for value in (False, None, 'unknown'):
            with self.subTest(value=value):
                self.e['cases'][0]['candidate']['objective_pass'] = value
                self.hold()

    def test_candidate_critical_failure_and_unknown_hold(self):
        for value in (['protected behavior changed'], None, 'unknown'):
            with self.subTest(value=value):
                self.e['cases'][0]['candidate']['critical_failures'] = value
                self.hold()

    def test_missing_objective_check_holds(self):
        del self.e['cases'][0]['candidate']['objective_pass']
        self.hold()

    def test_editor_cannot_generate(self):
        self.e['cases'][0]['candidate']['execution_id'] = self.e['creator_execution_id']
        self.hold()

    def test_cross_case_judge_cannot_generate(self):
        self.e['cases'][0]['judge']['execution_id'] = self.e['cases'][1]['candidate']['execution_id']
        self.hold()

    def test_unknown_model_is_exploratory_only(self):
        self.p['cases'][0]['conditions']['model'] = 'unknown'
        for v in ('baseline', 'candidate'):
            self.e['cases'][0][v]['conditions']['model'] = 'unknown'
        self.freeze()
        self.hold()

    def test_monitor_version_skill_task_grouping_and_attribution(self):
        base = {'correction_id': 'c1', 'skill': 'skill-a', 'task_class': 'edit', 'eligible': True, 'observed': True, 'result': 'correction', 'version_id': 'v2', 'observed_at': '2026-09-22T12:00:00Z', 'evidence': 'Observed correction with exact transcript reference.'}
        observations = [dict(base, observation_id='current'), dict(base, observation_id='old', version_id='v1'), dict(base, observation_id='other-skill', skill='skill-b'), dict(base, observation_id='other-task', task_class='review')]
        data = {'promotions': [{'correction_id': 'c1', 'skill': 'skill-a', 'version_id': 'v2', 'promoted_at': '2026-09-21T12:00:00Z'}], 'observations': observations}
        path = self.root / 'observations.json'
        path.write_text(json.dumps(data))
        result = gate.monitor(path)
        self.assertEqual(len(result['counts']), 4)
        self.assertTrue(all(c['corrections'] == 1 for c in result['counts']))
        self.assertEqual(result['aggregate']['corrections'], 4)
        self.assertEqual([e['observation_id'] for e in result['attribution_pending']], ['old'])
        self.assertNotIn('other-skill', [e['observation_id'] for e in result['reopened']])

    def test_monitor_promotion_requires_skill_and_version(self):
        path = self.root / 'observations.json'
        path.write_text(json.dumps({'promotions': [{'correction_id': 'c1', 'promoted_at': '2026-09-21T12:00:00Z'}], 'observations': []}))
        self.assertEqual(gate.monitor(path)['status'], 'hold')


if __name__ == '__main__':
    unittest.main()
