from pathlib import Path
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch
import vendor

class VendorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)/'vendor'
        shutil.copytree(vendor.VENDOR, self.root)
        self.patches = [patch.object(vendor, 'VENDOR', self.root), patch.object(vendor, 'MANIFEST', self.root/'manifest.json')]
        for p in self.patches: p.start()
    def tearDown(self):
        for p in self.patches: p.stop()
        self.tmp.cleanup()
    def test_recorded_copy_verifies(self):
        self.assertEqual([e['name'] for e in vendor.verify()['plugins']], ['seo'])
    def test_local_edit_detected(self):
        path = self.root/'seo/skills/seo/SKILL.md'
        path.write_text(path.read_text()+'\nlocal edit\n')
        with self.assertRaisesRegex(AssertionError, 'differ from the recorded'): vendor.verify()
    def test_unrecorded_plugin_detected(self):
        (self.root/'other/.claude-plugin').mkdir(parents=True)
        (self.root/'other/.claude-plugin/plugin.json').write_text(json.dumps({'name':'other','version':'1'}))
        with self.assertRaisesRegex(AssertionError, 'Vendor inventory changed'): vendor.verify()
    def test_top_level_bin_rejected(self):
        (self.root/'seo/bin').mkdir()
        with self.assertRaisesRegex(AssertionError, 'bin/'): vendor.verify()

if __name__ == '__main__': unittest.main()
