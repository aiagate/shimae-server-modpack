import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import diagnose_api as d


class AuditTests(unittest.TestCase):
    def test_one_get_resolves_only_exact_public_names_and_ids(self):
        factory = Mock()
        conn = factory.return_value
        response = conn.getresponse.return_value
        response.status = 200
        rows = [{'name': name, 'id': i + 1, 'gameVersionTypeID': i + 2,
                 'private': 'dummy-token user@example.invalid'} for i, name in enumerate(d.WANTED)]
        rows.append({'name': 'dummy-token', 'id': 4, 'gameVersionTypeID': 5})
        response.read.return_value = json.dumps(rows).encode()
        result = d.audit('dummy-token', factory)
        self.assertEqual(result['category'], 'all_metadata_names_exist')
        self.assertEqual(result['missing_names'], [])
        self.assertEqual(len(result['matched_versions']), 3)
        conn.request.assert_called_once_with('GET', '/api/game/versions',
                                            headers={'X-Api-Token': 'dummy-token'})
        conn.close.assert_called_once()
        for forbidden in ('dummy-token', 'user@example.invalid', 'private'):
            self.assertNotIn(forbidden, json.dumps(result))

    def test_missing_or_ambiguous_version_names_are_not_guessed(self):
        for rows, category in (([], 'missing_version_names'),
                               ([{'name': 'Client', 'id': 1, 'gameVersionTypeID': 2}] * 2,
                                'ambiguous_version_names')):
            factory = Mock()
            response = factory.return_value.getresponse.return_value
            response.status = 200
            response.read.return_value = json.dumps(rows).encode()
            self.assertEqual(d.audit('dummy-token', factory)['category'], category)
            factory.return_value.request.assert_called_once()

    def test_read_only_errors_are_sanitized_and_never_retry(self):
        factory = Mock()
        response = factory.return_value.getresponse.return_value
        response.status = 403
        response.read.return_value = b'{"errorCode":403,"errorMessage":"dummy-token user@example.invalid"}'
        result = d.audit('dummy-token', factory)
        self.assertEqual(result['http_status'], 403)
        self.assertEqual(result['response_summary']['error_code'], 403)
        self.assertNotIn('dummy-token', json.dumps(result))
        self.assertNotIn('user@example.invalid', json.dumps(result))
        factory.return_value.request.assert_called_once()
        with self.assertRaises(d.Invalid):
            d.audit('', factory)
        factory.return_value.request.assert_called_once()
