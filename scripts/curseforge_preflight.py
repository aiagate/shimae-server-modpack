"""Read-only Upload API version audit; no POST or private response text."""
import http.client
import ssl
from collections.abc import Callable

from curseforge_api import HOST, read_error_summary, token_check
from pack_validation import parse_json

WANTED = ('1.21.1', 'NeoForge', 'Client')
LIMIT = 2 * 1024 * 1024


def credential_preflight(token):
    """Boolean input properties only: no value, prefix, length or fingerprint.

    Upload API does not document a token-format discriminator. These properties
    can detect copying mistakes, but cannot prove Upload vs Core API origin.
    """
    return {'present': bool(token),
            'has_whitespace': any(c.isspace() for c in token),
            'has_control_characters': any(ord(c) < 32 or ord(c) == 127 for c in token),
            'has_non_ascii_characters': any(ord(c) >= 128 for c in token),
            'token_kind_verified_from_format': False}


def audit(token, connection_factory: Callable[..., http.client.HTTPSConnection] = http.client.HTTPSConnection):
    token_check(token)
    report = {'method': 'GET', 'path': '/api/game/versions', 'http_status': None,
              'status': 'unconfirmed', 'requested_names': list(WANTED),
              'matched_versions': [], 'missing_names': None,
              'credential_preflight': credential_preflight(token)}
    conn = None
    try:
        conn = connection_factory(HOST, timeout=30)
        conn.request('GET', '/api/game/versions', headers={'X-Api-Token': token})
        response = conn.getresponse()
        if type(response.status) is not int or not 100 <= response.status <= 599:
            report['category'] = 'invalid_http_status'
            return report
        report['http_status'] = response.status
        if not 200 <= response.status < 300:
            report.update(category='http_non_success', response_summary=read_error_summary(response, (token,)))
            return report
        raw = response.read(LIMIT + 1)
        if len(raw) > LIMIT:
            report['category'] = 'response_too_large'
            return report
        try:
            rows = parse_json(raw)
        except (ValueError, UnicodeError, RecursionError):
            report['category'] = 'invalid_json_response'
            return report
        if not isinstance(rows, list):
            report['category'] = 'invalid_versions_shape'
            return report
        for row in rows:
            if not isinstance(row, dict) or row.get('name') not in WANTED:
                continue
            if any(type(row.get(k)) is not int or not 0 < row[k] < 2**31
                   for k in ('id', 'gameVersionTypeID')):
                report['category'] = 'invalid_version_identifiers'
                return report
            report['matched_versions'].append({k: row[k] for k in ('name', 'id', 'gameVersionTypeID')})
        found = {row['name'] for row in report['matched_versions']}
        missing_names = [name for name in WANTED if name not in found]
        report.update(status='read_complete', missing_names=missing_names)
        # Upload metadata uses documented string names, never guessed numeric IDs.
        # A name may legitimately occur in multiple gameVersionTypeID groups.
        report['numeric_ids_selected'] = False
        if missing_names:
            report['category'] = 'missing_version_names'
        elif len(found) != len(report['matched_versions']):
            report['category'] = 'all_metadata_names_present_with_variants'
        else:
            report['category'] = 'all_metadata_names_exist'
        return report
    except ssl.SSLError:
        report['category'] = 'tls_error'
    except TimeoutError:
        report['category'] = 'timeout'
    except OSError:
        report['category'] = 'connection_error'
    except http.client.HTTPException:
        report['category'] = 'http_protocol_error'
    finally:
        if conn is not None:
            try:
                conn.close()
            except (OSError, http.client.HTTPException):
                pass
    return report
