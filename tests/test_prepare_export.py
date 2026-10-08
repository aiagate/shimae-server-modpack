"""Synthetic preparation fixtures: original bytes and live settings are preserved."""
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import prepare_export as p
import test_release


class PrepareExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'LICENSE').write_text('Synthetic license fixture.')
        (self.root / 'LICENSE-SCOPE.txt').write_text('Synthetic scope fixture.')
        self.blob, self.config = test_release.ReleaseTests().fixture({
            'overrides/config/current.toml': 'user_setting = 42',
            'overrides/config/sodium-fingerprint.json': '{"hash":"synthetic"}',
            'overrides/config/current-1.toml.bak': 'user_setting = 12'})
        sha = lambda data: hashlib.sha256(data).hexdigest()
        with zipfile.ZipFile(io.BytesIO(self.blob)) as z:
            self.plan = {'source_sha256': sha(self.blob), 'manifest_sha256': sha(z.read('manifest.json')),
                         'modlist_sha256': None, 'additions': p.ADDITIONS,
                         'omit_paths': ['overrides/config/sodium-fingerprint.json',
                                        'overrides/config/current-1.toml.bak']}
        # The fixture's optional modlist is added while keeping a real root layout.
        out = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(self.blob)) as z, zipfile.ZipFile(out, 'w') as dest:
            for name in z.namelist(): dest.writestr(name, z.read(name))
            dest.writestr('modlist.html', '<html>Synthetic test</html>')
        self.blob = out.getvalue();self.plan['source_sha256'] = sha(self.blob)
        self.plan['modlist_sha256'] = sha(b'<html>Synthetic test</html>')

    def test_only_reviewed_state_removed_manifest_modlist_settings_identical(self):
        before = self.blob
        clean = p.prepare(self.blob, self.plan, self.config, self.root)
        self.assertEqual(self.blob, before)
        with zipfile.ZipFile(io.BytesIO(before)) as original, zipfile.ZipFile(io.BytesIO(clean)) as prepared:
            self.assertEqual(prepared.read('manifest.json'), original.read('manifest.json'))
            self.assertEqual(prepared.read('modlist.html'), original.read('modlist.html'))
            self.assertEqual(prepared.read('overrides/config/current.toml'), b'user_setting = 42')
            self.assertFalse(set(self.plan['omit_paths']) & set(prepared.namelist()))
            self.assertEqual(prepared.read('overrides/LICENSE-Shimae.txt'), (self.root / 'LICENSE').read_bytes())
            self.assertIsNone(prepared.testzip())
        self.assertEqual(p.prepare(before, self.plan, self.config, self.root), clean)

    def test_changed_source_live_setting_removal_and_manifest_removal_rejected(self):
        with self.assertRaises(p.Invalid):
            p.prepare(self.blob + b'x', self.plan, self.config, self.root)
        for name in ['manifest.json', 'modlist.html', 'overrides/config/current.toml']:
            with self.subTest(name=name), self.assertRaises(p.Invalid):
                p.prepare(self.blob, dict(self.plan, omit_paths=[name]), self.config, self.root)

    def test_manifest_reference_hash_change_and_arbitrary_addition_rejected(self):
        with self.assertRaises(p.Invalid):
            p.prepare(self.blob, dict(self.plan, manifest_sha256='0' * 64), self.config, self.root)
        with self.assertRaises(p.Invalid):
            p.prepare(self.blob, dict(self.plan, additions={'overrides/secret.txt': '.env'}), self.config, self.root)


if __name__ == '__main__':
    unittest.main()
