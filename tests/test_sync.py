from pathlib import Path
import json
import tempfile
import shutil
import subprocess
import sys
import os
import unittest
from unittest.mock import patch
import sync

class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.target = Path(self.tmp.name)/'skills'
    def tearDown(self):
        self.tmp.cleanup()
    def test_install_update_conflict_and_unrelated_preservation(self):
        self.target.mkdir()
        (self.target/'other').mkdir()
        (self.target/'other/keep').write_text('keep')
        result = sync.install('codex', self.target)
        self.assertEqual(result['status'], 'current')
        self.assertEqual(sync.install('codex', self.target)['status'], 'current')
        path = self.target/'copy-reviewer/SKILL.md'
        path.write_text(path.read_text()+'\nlocal improvement\n')
        with self.assertRaises(ValueError): sync.install('codex', self.target)
        self.assertIn('local improvement', path.read_text())
        self.assertEqual((self.target/'other/keep').read_text(), 'keep')
    def test_unmanaged_collision(self):
        (self.target/'copy-reviewer').mkdir(parents=True)
        with self.assertRaises(ValueError): sync.install('codex', self.target)
    def test_code_package(self):
        self.assertEqual(sync.install('code', self.target)['status'], 'current')
        self.assertTrue((self.target/'agents/artifact-reviewer.md').is_file())
        self.assertTrue((self.target/'skills/learning-loop/SKILL.md').is_file())
    def test_deleted_managed_file_is_conflict(self):
        sync.install('codex', self.target)
        (self.target/'learning-loop/SKILL.md').unlink()
        self.assertEqual(sync.state('codex', self.target)[3]['status'], 'conflict')
    def test_rollback_on_failed_install(self):
        sync.install('codex', self.target)
        before = sync.inventory(self.target)
        r=json.loads((self.target/sync.RECEIPT).read_text())
        r['input_sha256']='old'
        (self.target/sync.RECEIPT).write_text(json.dumps(r))
        before = sync.inventory(self.target)
        original = Path.rename
        def fail(p, destination):
            if p.parent.name == 'new' and p.name == 'learning-loop':
                raise OSError('simulated disk failure')
            return original(p, destination)
        with patch.object(Path, 'rename', fail):
            with self.assertRaises(OSError): sync.install('codex', self.target)
        self.assertEqual(sync.inventory(self.target), before)
    def test_failed_rollback_preserves_recovery_files(self):
        sync.install('codex', self.target)
        r=json.loads((self.target/sync.RECEIPT).read_text())
        r['input_sha256']='old'
        (self.target/sync.RECEIPT).write_text(json.dumps(r))
        original = Path.rename
        def fail(p, destination):
            if (p.parent.name == 'new' and p.name == 'learning-loop') or p.parent.name == 'old':
                raise OSError('simulated persistent disk failure')
            return original(p, destination)
        with patch.object(Path, 'rename', fail):
            with self.assertRaisesRegex(OSError, 'preserved recovery files'):
                sync.install('codex', self.target)
        stages=list(Path(self.tmp.name).glob('.oakheart-stage-*'))
        self.assertEqual(len(stages), 1)
        self.assertTrue((stages[0]/'old/learning-loop/SKILL.md').is_file())
    def test_unregistered_source_skill_fails_build(self):
        repo=Path(self.tmp.name)/'repo'
        shutil.copytree(sync.ROOT, repo, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        extra=repo/'source/new-skill'
        extra.mkdir()
        (extra/'SKILL.md').write_text('---\nname: new-skill\ndescription: Test\n---\n')
        before=sync.inventory(repo/'dist')
        result=subprocess.run([sys.executable, 'build.py'], cwd=repo, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sync.inventory(repo/'dist'), before)
    def test_interrupt_restores_installation(self):
        sync.install('codex', self.target)
        r=json.loads((self.target/sync.RECEIPT).read_text());r['input_sha256']='old'
        (self.target/sync.RECEIPT).write_text(json.dumps(r))
        before=sync.inventory(self.target)
        original=Path.rename
        def interrupt(p, destination):
            if p.parent.name == 'new' and p.name == 'learning-loop': raise KeyboardInterrupt()
            return original(p,destination)
        with patch.object(Path,'rename',interrupt):
            with self.assertRaises(KeyboardInterrupt): sync.install('codex',self.target)
        self.assertEqual(sync.inventory(self.target),before)
    def test_edit_during_staging_is_preserved(self):
        sync.install('codex', self.target)
        r=json.loads((self.target/sync.RECEIPT).read_text());r['input_sha256']='old'
        (self.target/sync.RECEIPT).write_text(json.dumps(r))
        original=shutil.copytree
        changed=False
        def edit(*args, **kwargs):
            nonlocal changed
            if not changed:
                changed=True
                (self.target/'copy-reviewer/SKILL.md').write_text('concurrent edit')
            return original(*args,**kwargs)
        with patch.object(shutil,'copytree',edit):
            with self.assertRaisesRegex(ValueError,'Destination changed'): sync.install('codex',self.target)
        self.assertEqual((self.target/'copy-reviewer/SKILL.md').read_text(),'concurrent edit')
    def test_concurrent_installer_refused(self):
        lock=self.target.parent/('.oakheart-'+self.target.name+'.lock')
        lock.write_text('locked')
        with self.assertRaisesRegex(ValueError,'Installation locked'): sync.install('codex',self.target)
        self.assertTrue(lock.exists())
    def test_symlinks_and_managed_host_rejected(self):
        link=Path(self.tmp.name)/'link'
        link.symlink_to(Path(self.tmp.name), target_is_directory=True)
        with self.assertRaises(ValueError): sync.safe_target(link/'skills')
        with self.assertRaises(ValueError): sync.safe_target(Path(self.tmp.name)/'remote-skills')
    def test_malformed_receipt_rejected(self):
        self.target.mkdir()
        (self.target/sync.RECEIPT).write_text(json.dumps({'platform':'codex','units':{'../outside':{}}}))
        with self.assertRaises(ValueError): sync.state('codex', self.target)

if __name__ == '__main__': unittest.main()
