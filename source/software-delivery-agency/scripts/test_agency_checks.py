import copy
import unittest
from agency_checks import check, sample_size, STAGES, SURFACES


class ChecksTests(unittest.TestCase):
    def test_reference_plan(self):
        r = sample_size(.02, .03, 1000)
        self.assertEqual(r["total_visitors"], 7652)
        self.assertEqual(r["estimated_months"], 7.65)
        self.assertEqual(r["relative_lift_percent"], 50)

    def test_smaller_effect_needs_more_traffic(self):
        self.assertGreater(sample_size(.02, .024)["total_visitors"], sample_size(.02, .03)["total_visitors"])

    def test_reject_invalid_plans(self):
        for b,t,v in [(0,.03,100),(.03,.02,100),(.02,1,100),(.02,.03,0),(float('nan'),.03,100),(.02,.03,float('inf'))]:
            with self.assertRaises(ValueError):
                sample_size(b,t,v)

    def record(self):
        ids = STAGES['release'] + SURFACES['booking']
        return {"schema_version":1,"release_id":"r2","surfaces":["booking"],"evidence":{
            k:{"status":"verified","artifact":"fixture://"+k,"observed_at":"2026-09-13","reviewer":"fixture","release_id":"r2"} for k in ids}}

    def test_booking_happy_and_missing_webhook(self):
        r=self.record()
        self.assertTrue(check(r,'release')['evidence_complete'])
        del r['evidence']['webhook_dedup']
        self.assertIn('webhook_dedup',check(r,'release')['missing'])

    def test_stale_evidence_does_not_cover_new_version(self):
        r=self.record(); r['release_id']='r3'
        self.assertFalse(check(r,'release')['evidence_complete'])

    def test_self_attested_pass_without_artifact_fails(self):
        r=self.record(); r['evidence']['payment_states'].pop('artifact')
        self.assertFalse(check(r,'release')['evidence_complete'])

    def test_empty_and_unknown_surfaces(self):
        r=self.record(); r['surfaces']=[]
        self.assertFalse(check(r,'release')['evidence_complete'])
        r['surfaces']=['checkout']
        with self.assertRaises(ValueError): check(r,'release')

    def test_read_only_and_no_payment_decision(self):
        r=self.record(); before=copy.deepcopy(r)
        result=check(r,'release')
        self.assertEqual(r,before)
        self.assertNotIn('authorized',result)


if __name__ == '__main__':
    unittest.main()
