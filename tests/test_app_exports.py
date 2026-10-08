"""Synthetic exports only: no App provenance or real MOD runtime claim."""
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import verify_app_exports as v
import test_release


class AppExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.exports = self.root / 'exports'
        self.exports.mkdir()
        self.blobs = {}
        self.refs = {}
        self.lock = {'schema_version': 1, 'repository': v.fetch_export.REPOSITORY,
                     'version': 'test', 'minecraft_version': 'test-version',
                     'mod_loader': 'forge-test-loader', 'profiles': {}}
        self.policy = {'schema_version': 1, 'forbidden_project_ids': [302973, 1546772, 278993],
                       'retained_project_ids': [1], 'client_only_project_ids': [3],
                       'expected_counts': {'client': 3, 'server': 2},
                       'commented_json_paths': [], 'override_sha256': {}}
        for kind, count, asset in [('client', 3, 1010), ('server', 2, 2020)]:
            files = [{'projectID': i, 'fileID': i + 100, 'required': True, 'isLocked': False}
                     for i in range(1, count + 1)]
            blob, config = test_release.ReleaseTests().fixture(
                {'overrides/config/example.toml': 'enabled = true'},
                change=lambda m, files=files: m.update(files=files))
            self.blobs[kind] = blob
            self.refs[kind] = {'files': files, 'basis': 'Synthetic fixture'}
            self.lock['profiles'][kind] = {
                'asset_id': asset, 'filename': f'synthetic-test-{kind}.zip',
                'size_bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest(),
                'manifest_name': 'Synthetic test', 'reference_lock': f'exports/{kind}.refs.json',
                'origin': {'exporter': 'CurseForge App', 'confirmed': True,
                           'confirmed_by': 'Synthetic fixture only', 'exported_at': 'test',
                           'source_profile': 'Synthetic fixture only'}}
            self.policy['override_sha256'][kind] = {
                'overrides/config/example.toml': hashlib.sha256(b'enabled = true').hexdigest()}
        self.config = dict(config, project_id=1733082, export_asset_id=1010,
                           reviewed_sha256=self.lock['profiles']['client']['sha256'])
        self.save()

    def save(self):
        for name, value in [('exports.lock.json', self.lock), ('policy.json', self.policy),
                            ('client.refs.json', self.refs['client']), ('server.refs.json', self.refs['server'])]:
            (self.exports / name).write_text(json.dumps(value))
        (self.root / 'release.json').write_text(json.dumps(self.config))

    def load(self):
        self.save()
        return v.load_inputs(self.exports / 'exports.lock.json', self.exports / 'policy.json',
                             self.root / 'release.json')

    def cli(self, *options):
        args = ['verify_app_exports.py', '--lock', str(self.exports / 'exports.lock.json'),
                '--policy', str(self.exports / 'policy.json'), '--release-config',
                str(self.root / 'release.json'), *map(str, options)]
        with patch.object(sys, 'argv', args):
            return v.main()

    def mutate(self, kind, edits):
        out = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(self.blobs[kind])) as source, zipfile.ZipFile(out, 'w') as dest:
            contents = {n: source.read(n) for n in source.namelist()}
            contents.update(edits)
            for name, body in contents.items():
                dest.writestr(name, body)
        self.blobs[kind] = out.getvalue()
        item = self.lock['profiles'][kind]
        item['size_bytes'] = len(self.blobs[kind])
        item['sha256'] = hashlib.sha256(self.blobs[kind]).hexdigest()
        if kind == 'client':
            self.config['reviewed_sha256'] = item['sha256']

    def test_complete_pair_and_exact_byte_preservation(self):
        self.load()
        out = self.root / 'out'
        github_output = self.root / 'outputs'
        with patch.object(v.fetch_export, 'fetch', side_effect=[self.blobs[k] for k in v.KINDS]) as fetch:
            self.assertEqual(self.cli('--fetch', '--output', out, '--commit', 'a' * 40,
                                      '--github-output', github_output), 0)
        for index, kind in enumerate(v.KINDS):
            item = self.lock['profiles'][kind]
            self.assertEqual((out / item['filename']).read_bytes(), self.blobs[kind])
            self.assertEqual(fetch.call_args_list[index].kwargs,
                             {'expected_name': item['filename'], 'expected_size': item['size_bytes']})
        receipt = json.loads((out / 'receipt.json').read_text())
        self.assertEqual(receipt['project_id'], 1733082)
        self.assertEqual(receipt['app_origin'], 'human-confirmed; not machine-proven')
        self.assertIn('client_zip=', github_output.read_text())
        self.assertIn('server_zip=', github_output.read_text())

    def test_pending_origin_blocks_network_and_manual_but_pr_state_is_explicit(self):
        self.lock['profiles']['server']['origin']['confirmed'] = False
        self.save()
        with patch.object(v.fetch_export, 'fetch') as fetch:
            out = self.root / 'pending'
            self.assertEqual(self.cli('--fetch', '--output', out, '--commit', 'a' * 40), 1)
            outputs = self.root / 'outputs'
            self.assertEqual(self.cli('--check-state', '--github-output', outputs), 0)
            self.assertEqual(outputs.read_text(), 'ready=false\n')
            self.assertFalse(out.exists())
            fetch.assert_not_called()

    def test_repository_configuration_is_consistent_in_pending_or_ready_state(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(json.loads((root / 'release.json').read_text())['project_id'], 1733082)
        try:
            v.load_inputs(root / 'exports/exports.lock.json', root / 'exports/policy.json', root / 'release.json')
        except v.InputWait:
            pass  # Future real App exports can populate this same configuration.

    def test_changed_sha_identity_and_reference_fail(self):
        lock, policy, refs, configs = self.load()
        for kind in v.KINDS:
            with self.subTest(kind=kind), self.assertRaises(v.Invalid):
                v.check_blob(self.blobs[kind][:-1] + b'x', kind, lock, policy, refs, configs[kind])
        self.lock['profiles']['client']['manifest_name'] = 'Different profile'
        lock, policy, refs, configs = self.load()
        with self.assertRaises(v.Invalid):
            v.check_blob(self.blobs['client'], 'client', lock, policy, refs, configs['client'])
        self.lock['profiles']['client']['manifest_name'] = 'Synthetic test'
        self.refs['client']['files'][-1]['fileID'] += 1
        lock, policy, refs, configs = self.load()
        with self.assertRaises(v.Invalid):
            v.check_blob(self.blobs['client'], 'client', lock, policy, refs, configs['client'])

    def test_cross_profile_mismatch_removed_and_retained_mods(self):
        original = copy.deepcopy(self.refs)
        for change in ('shared', 'forbidden', 'retained', 'client-only'):
            self.refs = copy.deepcopy(original)
            if change == 'shared':
                self.refs['server']['files'][0]['fileID'] += 1
            elif change == 'forbidden':
                self.refs['client']['files'][-1]['projectID'] = 302973
            elif change == 'retained':
                self.refs['server']['files'][0]['projectID'] = 4
            else:
                self.refs['client']['files'][-1]['projectID'] = 4
            with self.subTest(change=change), self.assertRaises(v.Invalid):
                self.load()

    def test_release_lock_mismatch_and_bad_assets_fail_before_fetch(self):
        original = copy.deepcopy(self.lock)
        for field, value in [('filename', '../escape.zip'), ('filename', 'test\nclient.zip'),
                             ('asset_id', True), ('sha256', 'x' * 64), ('size_bytes', v.MAX_ZIP + 1)]:
            self.lock = copy.deepcopy(original)
            self.lock['profiles']['client'][field] = value
            with self.subTest(field=field), self.assertRaises(v.Invalid):
                self.load()
        self.lock = original
        self.config['reviewed_sha256'] = '0' * 64
        with self.assertRaises(v.Invalid):
            self.load()

    def test_personal_state_credentials_and_tfc_namespaces_are_rejected(self):
        original_blobs = copy.deepcopy(self.blobs)
        for name, content in [('overrides/config/sodium-fingerprint.json', '{}'),
                              ('overrides/config/chunky/overworld.csv', 'state'),
                              ('overrides/config/gpushift/benchmarks/a.txt', 'state'),
                              ('overrides/config/bonsaitrees4-common.toml', 'enabled = true'),
                              ('overrides/config/example.toml', 'api_key="dummy-not-real"'),
                              ('overrides/config/example.toml', 'block = "tfc:stone"')]:
            self.blobs = copy.deepcopy(original_blobs)
            self.mutate('client', {name: content})
            lock, policy, refs, configs = self.load()
            with self.subTest(name=name), self.assertRaises(v.Invalid):
                v.check_blob(self.blobs['client'], 'client', lock, policy, refs, configs['client'])

    def test_shared_override_policy_mismatch_is_rejected(self):
        self.policy['override_sha256']['server']['overrides/config/example.toml'] = '0' * 64
        with self.assertRaises(v.Invalid):
            self.load()

    def test_bad_second_export_never_saves_first_export_or_report(self):
        out = self.root / 'failed'
        with patch.object(v.fetch_export, 'fetch', side_effect=[self.blobs['client'], b'bad']):
            self.assertEqual(self.cli('--fetch', '--output', out, '--commit', 'a' * 40), 1)
        self.assertFalse(out.exists())

    def test_submission_recheck_client_only_does_not_fetch_or_rewrite_zip(self):
        root = self.root / 'downloaded'
        root.mkdir()
        path = root / self.lock['profiles']['client']['filename']
        path.write_bytes(self.blobs['client'])
        outputs = self.root / 'outputs'
        with patch.object(v.fetch_export, 'fetch') as fetch:
            self.assertEqual(self.cli('--directory', root, '--profile', 'client', '--github-output', outputs), 0)
            fetch.assert_not_called()
        self.assertEqual(path.read_bytes(), self.blobs['client'])
        self.assertEqual(outputs.read_text(), f'client_zip={path.resolve()}\n')

    def test_local_checks_before_publication_allow_null_asset_ids_but_fetch_waits(self):
        paths = {}
        for kind in v.KINDS:
            self.lock['profiles'][kind]['asset_id'] = None
            paths[kind] = self.root / self.lock['profiles'][kind]['filename']
            paths[kind].write_bytes(self.blobs[kind])
        self.config['export_asset_id'] = None
        self.save()
        with patch.object(v.fetch_export, 'fetch') as fetch:
            self.assertEqual(self.cli('--client', paths['client'], '--server', paths['server']), 0)
            self.assertEqual(self.cli('--fetch', '--output', self.root / 'out', '--commit', 'a' * 40), 1)
            fetch.assert_not_called()

    def test_bad_toml_even_with_reviewed_hash_is_rejected(self):
        content = 'enabled = [invalid'
        self.mutate('client', {'overrides/config/example.toml': content})
        for kind in v.KINDS:
            self.policy['override_sha256'][kind]['overrides/config/example.toml'] = hashlib.sha256(content.encode()).hexdigest()
        lock, policy, refs, configs = self.load()
        with self.assertRaises(ValueError):
            v.check_blob(self.blobs['client'], 'client', lock, policy, refs, configs['client'])


if __name__ == '__main__':
    unittest.main()
