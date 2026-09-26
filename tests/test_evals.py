from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('eval_common',Path(__file__).parents[1]/'evals/common.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)

class EvalTests(unittest.TestCase):
    def test_no_overwrite_or_stale_cache(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'result.json';e.write(p,{'version':1})
            with self.assertRaises(FileExistsError):e.write(p,{'version':2})
            self.assertEqual(json.loads(p.read_text()),{'version':1})
    def test_success_and_trace(self):
        events=[{'type':'assistant','message':{'model':'model-v1','content':[{'type':'tool_use','name':'Skill','input':{'skill':'oakheart:copy-reviewer'}}]}},{'type':'result','result':'answer','is_error':False}]
        r=e.parse_stream('\n'.join(map(json.dumps,events)),0)
        self.assertTrue(r['valid']);self.assertEqual(r['observed_models'],['model-v1']);self.assertEqual(len(r['calls']),1)
    def test_tool_failure_invalidates_answer(self):
        events=[{'type':'user','message':{'content':[{'type':'tool_result','is_error':True,'content':'read denied'}]}},{'type':'result','result':'I guessed','is_error':False}]
        self.assertFalse(e.parse_stream('\n'.join(map(json.dumps,events)),0)['valid'])
    def test_error_empty_and_permission_denial(self):
        for event,code in [({'type':'result','result':'answer'},1),({'type':'result','result':''},0),({'type':'result','result':'answer','permission_denials':[{}]},0),({'type':'result','result':'answer','is_error':True},0)]:
            self.assertFalse(e.parse_stream(json.dumps(event),code)['valid'])
        self.assertFalse(e.parse_stream('',0)['valid'])
    def test_order_disagreement_not_two_wins(self):
        self.assertEqual(e.combine_orders([{'order':'AB','preference':'candidate'},{'order':'BA','preference':'baseline'}]),'order_sensitive')
        self.assertEqual(e.combine_orders([{'order':'AB','preference':'candidate'}]),'incomplete')
        self.assertEqual(e.combine_orders([{'order':'AB','preference':'candidate'},{'order':'BA','preference':'candidate'}]),'candidate')
    def test_changed_frozen_input_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'plugin').mkdir();(p/'plugin/a').write_text('before')
            e.write(p/'manifest.json',{'frozen':{'plugin':e.files_digest(p/'plugin')}})
            e.verify_frozen(p);(p/'plugin/a').write_text('after')
            with self.assertRaises(ValueError):e.verify_frozen(p)
    def test_malformed_events_retained_as_invalid(self):
        final=json.dumps({'type':'result','result':'answer'})
        for bad in ['[]','null','"bad"','not json',json.dumps({'type':'assistant','message':None}),json.dumps({'type':'assistant','message':{'content':[None]}})]:
            r=e.parse_stream(bad+'\n'+final,0)
            self.assertFalse(r['valid']);self.assertTrue(r['unparsed_lines'])
    def test_missing_pairs_stay_in_denominator(self):
        import sys
        sys.modules['common']=e
        spec=importlib.util.spec_from_file_location('eval_analyze',Path(__file__).parents[1]/'evals/analyze.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        m={'jobs':[['task','baseline',0],['task','plugin',0],['task','forced',0]]}
        r=module.summarize(m,{})
        self.assertEqual(r['plugin']['expected_pairs'],1);self.assertEqual(r['plugin']['missing_pairs'],1)
        records={('task','plugin',0,o):{'status':'blocked_run'} for o in ['AB','BA']}
        self.assertEqual(module.summarize(m,records)['plugin']['blocked_or_invalid_pairs'],1)
    def test_mocked_full_experiment_and_fresh_rerun(self):
        import os,subprocess,sys
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);binpath=root/'bin';binpath.mkdir()
            cli=binpath/'claude'
            cli.write_text('#!'+sys.executable+'\nimport sys,json\nif "--version" in sys.argv: print("mock-cli-test-only");sys.exit()\nprompt=sys.argv[sys.argv.index("-p")+1]\nanswer="test answer"\nif "Evaluate two answers blind" in prompt:\n answer=json.dumps({"preference":"tie","A":{"overall":7,"critical_fail":False,"unsupported_claims":[],"unverified":[]},"B":{"overall":7,"critical_fail":False,"unsupported_claims":[],"unverified":[]},"reason":"synthetic fixture"})\nprint(json.dumps({"type":"result","result":answer,"is_error":False}))\n')
            cli.chmod(0o755)
            tasks=root/'tasks.json';tasks.write_text(json.dumps([{'id':'fixture','skill':'copy-reviewer','prompt':'test','rubric':['test'],'critical':'none'}]))
            env=dict(os.environ);env['PATH']=str(binpath)+os.pathsep+env['PATH']
            scripts=Path(__file__).parents[1]/'evals'
            for _ in range(2):subprocess.run([sys.executable,str(scripts/'run.py'),'--model','mock','--tasks',str(tasks),'--reps','1','--output-root',str(root/'outputs')],env=env,check=True,capture_output=True)
            experiments=list((root/'outputs').iterdir());self.assertEqual(len(experiments),2)
            exp=experiments[0]
            subprocess.run([sys.executable,str(scripts/'judge.py'),'--model','mock','--experiment',str(exp)],env=env,check=True,capture_output=True)
            batch=next((exp/'judgments').iterdir())
            result=subprocess.run([sys.executable,str(scripts/'analyze.py'),'--batch',str(batch)],env=env,check=True,capture_output=True,text=True)
            counts=json.loads(result.stdout)['pair_counts_by_condition']
            self.assertEqual(counts['plugin']['tie'],1);self.assertEqual(counts['forced']['tie'],1)
    def test_symlink_snapshot_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'a').write_text('data');(p/'b').symlink_to(p/'a')
            with self.assertRaises(ValueError):e.files_digest(p)

if __name__=='__main__':unittest.main()
