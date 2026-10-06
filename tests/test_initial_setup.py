"""Prove the untouched starter cannot download or submit a release."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import fetch_export as f
import release as r
import test_release as fixtures


class InitialSetupTests(unittest.TestCase):
    def setUp(self):
        self.example = json.loads((Path(__file__).resolve().parents[1] /
                                   'release.example.json').read_text())

    def test_unconfigured_example_stops_before_download(self):
        factory = Mock()
        with self.assertRaises(r.Invalid):
            f.fetch(self.example, factory)
        factory.assert_not_called()

    def test_unconfigured_example_cli_stops_before_download_save_and_submit(self):
        blob, _ = fixtures.ReleaseTests().fixture()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'example.json').write_text(json.dumps(self.example))
            (root / 'synthetic.zip').write_bytes(blob)
            output = root / 'download.zip'
            with patch.object(sys, 'argv', ['fetch_export.py', '--config',
                    str(root / 'example.json'), '--output', str(output)]), \
                    patch.object(f, 'get') as get:
                self.assertEqual(f.main(), 1)
                get.assert_not_called()
                self.assertFalse(output.exists())
            with patch.object(sys, 'argv', ['release.py', '--zip',
                    str(root / 'synthetic.zip'), '--config', str(root / 'example.json'),
                    '--submit']), patch.object(r, 'submit') as send:
                self.assertEqual(r.main(), 1)
                send.assert_not_called()
