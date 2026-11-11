import datetime as dt
from pathlib import Path
import re
import tempfile
import unittest
from automation.council import GateError, Supervisor, latest, source_snapshot, strict_json, validate_manifest, write_snapshot

class CouncilTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'project';self.root.mkdir()
        write_snapshot(self.root,{'klayer/core.py':'VALUE = 1\n','tests/test_core.py':'# pinned legacy assertion\n','README.md':'Original\n'})
        self.run=self.root/'.council-runs/test-run'
        self.deadline=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat()
    def fake(self,role,prompt,schema):
        if role.startswith('proposal'):return {'task':'Add helper','reason':'bounded','acceptance':['legacy remains']}
        if role=='adjudicator':return {'decision':'build','task':'add helper','reason':'small slice','acceptance':['legacy remains']}
        if role=='builder':return {'files':[{'path':'klayer/core.py','content':'VALUE = 1\ndef helper(): return 2\n'}],'summary':'helper'}
        return {'diff_hash':re.search(r'"diff_hash": "([0-9a-f]+)"',prompt).group(1),'verdict':'approve','findings':[]}
    def supervisor(self,model=None,test=None,**kw):
        return Supervisor(self.root,self.run,model_call=model or self.fake,test_call=test or (lambda p:{'passed':True,'commands':[],'mode':'test_fake'}),deadline=kw.pop('deadline',self.deadline),**kw)
    def test_reject_forbidden_paths(self):
        for path in ['../x.py','/tmp/x.py','.env','automation/council.py','data/x.json','klayer/../tests/a.py','klayer/.env.py','klayer\\x.py']:
            with self.subTest(path=path),self.assertRaises(GateError):validate_manifest(self.root,[{'path':path,'content':'x'}])
    def test_duplicate_and_size_gates(self):
        with self.assertRaises(GateError):validate_manifest(self.root,[{'path':'klayer/a.py','content':'1'},{'path':'klayer/a.py','content':'2'}])
        with self.assertRaises(GateError):validate_manifest(self.root,[{'path':'klayer/a.py','content':'x'*500001}])
    def test_symlink_and_hardlink_gates(self):
        import os
        outside=Path(self.temp.name)/'outside';outside.mkdir()
        (self.root/'klayer/link').symlink_to(outside,target_is_directory=True)
        with self.assertRaises(GateError):validate_manifest(self.root,[{'path':'klayer/link/x.py','content':'x'}])
        self.assertFalse((outside/'x.py').exists())
        os.link(self.root/'klayer/core.py',self.root/'klayer/linked.py')
        with self.assertRaises(GateError):validate_manifest(self.root,[{'path':'klayer/linked.py','content':'x'}])
    def test_strict_json(self):
        for raw in ['{"ok":true,"ok":false}','{} {}']:
            with self.assertRaises((GateError,ValueError)):strict_json(raw)
    def test_accepted_release_preserves_original(self):
        before=source_snapshot(self.root);s=self.supervisor();state=s.run_council('goal',rounds=1)
        self.assertEqual(state['accepted'],1);self.assertEqual(source_snapshot(self.root),before)
        ptr=latest(self.root);self.assertIn('def helper()',Path(ptr['release'],'klayer/core.py').read_text())
        self.assertEqual((self.run/'pinned-tests/test_core.py').read_text(),before['tests/test_core.py'])
        self.assertEqual(ptr['acceptance'],'manual_and_semantic_evaluation_still_required');self.assertEqual(s.calls,6)
    def test_failed_tests_do_not_publish(self):
        state=self.supervisor(test=lambda p:{'passed':False,'commands':[{'exit_code':1}]}).run_council('goal',rounds=1)
        self.assertEqual(state['accepted'],0);self.assertFalse((self.root/'.council-runs/latest-approved.json').exists())
        self.assertEqual((self.root/'klayer/core.py').read_text(),'VALUE = 1\n')
    def test_review_hash_must_match(self):
        def model(role,prompt,schema):
            obj=self.fake(role,prompt,schema)
            if role=='integrity-review':obj['diff_hash']='wrong'
            return obj
        self.assertEqual(self.supervisor(model=model).run_council('goal',rounds=1)['accepted'],0)
    def test_external_source_edit_is_not_overwritten(self):
        def model(role,prompt,schema):
            if role=='builder':(self.root/'README.md').write_text('User edit\n')
            return self.fake(role,prompt,schema)
        state=self.supervisor(model=model).run_council('goal',rounds=1)
        self.assertEqual(state['status'],'external_source_change');self.assertEqual((self.root/'README.md').read_text(),'User edit\n')
    def test_candidate_mutation_rejected(self):
        def test(stage):
            if stage.name=='candidate':(stage/'klayer/core.py').write_text('VALUE = 999\n')
            return {'passed':True}
        self.assertEqual(self.supervisor(test=test).run_council('goal',rounds=1)['accepted'],0)
    def test_unlisted_file_rejected(self):
        def test(stage):
            if stage.name=='candidate':(stage/'sitecustomize.py').write_text('bad')
            return {'passed':True}
        self.assertEqual(self.supervisor(test=test).run_council('goal',rounds=1)['accepted'],0)
    def test_budget_deadline_cancellation(self):
        s=self.supervisor(max_calls=1);state=s.run_council('goal',rounds=1)
        self.assertEqual(state['status'],'call_budget');self.assertLessEqual(s.calls,1)
        s=self.supervisor(deadline='2000-01-01T00:00:00+00:00');self.assertEqual(s.run_council('goal')['status'],'deadline')
        s=self.supervisor();s.cancel.set();self.assertEqual(s.run_council('goal')['status'],'cancelled')
    def test_only_one_controller(self):
        a=self.supervisor();b=self.supervisor();a.acquire()
        try:
            with self.assertRaises(GateError):b.acquire()
        finally:a.lock.close()
    def test_release_tamper_detected(self):
        self.supervisor().run_council('goal',rounds=1)
        release=Path(latest(self.root)['release']);(release/'klayer/core.py').write_text('tampered')
        with self.assertRaises(GateError):latest(self.root)
if __name__=='__main__':unittest.main()
