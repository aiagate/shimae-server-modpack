"""CurseForge Upload API metadata, token checks, and redacted errors."""
import http.client
import re

from pack_validation import Invalid, need, parse_json

HOST = 'minecraft.curseforge.com'


class SubmissionError(Invalid):
    """Bounded allowlisted diagnostics; never retain raw bodies or exceptions."""

    def __init__(self, category, phase, http_status=None, response_summary=None):
        self.diagnostics: dict[str, object] = {
            'category': category, 'phase': phase,
            'http_status': http_status, 'response_body_recorded': False,
        }
        if response_summary is not None:
            self.diagnostics['response_summary'] = response_summary
        status = f', HTTP {http_status}' if http_status is not None else ''
        super().__init__(f'Submission not confirmed ({category}, {phase}{status}). '
                         'Check author dashboard before any manual retry.')


def metadata(config, changelog):
    need(changelog.strip() and 'REPLACE_ME' not in changelog and len(changelog.encode()) <= 100000,
         'write a release changelog (up to 100 KB)')
    return {'changelog': changelog, 'changelogType': 'markdown',
            'displayName': config['display_name'], 'releaseType': config['release_type'],
            'gameVersionNames': config['game_version_names'], 'isMarkedForManualRelease': True}


def token_check(token):
    need(token and token.strip() == token and not any(ord(c) < 32 for c in token),
         'CURSEFORGE_API_TOKEN is not configured or invalid')


ERROR_FIELDS = frozenset(('metadata', 'file', 'projectId', 'projectID', 'changelog',
                         'changelogType', 'displayName', 'gameVersions', 'gameVersionNames',
                         'releaseType', 'isMarkedForManualRelease', 'parentFileID', 'relations'))
ERROR_CODES = frozenset(('required', 'invalid', 'invalid_value', 'not_found',
                        'unknown_game_version', 'invalid_game_version', 'invalid_release_type',
                        'invalid_metadata', 'project_not_approved', 'bad_request',
                        'unauthorized', 'forbidden', 'invalid_api_token', 'token_expired'))
MESSAGE_HINTS = {
    'malformed_authentication': re.compile(r'(?:parse|decode|malformed|format).{0,40}(?:token|api.?key)|'
                                         r'(?:token|api.?key).{0,40}(?:parse|decode|malformed|format)'),
    'invalid_authentication': re.compile(r'(?:invalid|expired|revoked|not valid).{0,40}(?:token|api.?key)|'
                                         r'(?:token|api.?key).{0,40}(?:invalid|expired|revoked|not valid)'),
    'missing_authentication': re.compile(r'(?:missing|required|not provided).{0,40}(?:token|api.?key)|'
                                         r'(?:token|api.?key).{0,40}(?:missing|required|not provided)'),
    'invalid_header': re.compile(r'(?:invalid|malformed).{0,40}header|header.{0,40}(?:invalid|malformed)'),
    'invalid_game_version': re.compile(r'(?:invalid|unknown|not found).{0,40}game.?version|'
                                      r'game.?version.{0,40}(?:invalid|unknown|not found)'),
    'project_not_approved': re.compile(r'project.{0,40}(?:not approved|unapproved|pending approval)'),
}


# Known protocol vocabulary only. Unknown reflected values are never retained.
ERROR_MESSAGE_WORDS = set(('a an the this that of to for from as at by in on with and or but '
    'is are was were be been being not no only must should can cannot could may will '
    'file files parent child project projects upload uploaded uploading additional server pack '
    'invalid valid validation error errors failed failure required missing found exist exists '
    'does do have has already duplicate approved approval rejected pending processing review '
    'status id ids metadata game version versions name names release type changelog extension '
    'permission permissions authorized unauthorized authentication api token key credentials '
    'provided specified supported unsupported allowed notallowed empty null request response '
    'size large small length limit exceeds contain contains expected match matches belong belongs '
    'use used set value values Please please try again before after until wait needs need '
    'parentfileid isserverpack gameversions gameversionnames releasetype displayname '
    'changelogtype ismarkedformanualrelease minecraft neoforge client').lower().split())


def diagnostic_message(message, secrets=()):
    if not isinstance(message,str) or len(message)>4096:
        return None
    for secret in secrets:
        if secret:
            message=message.replace(secret,'[redacted]')
    message=re.sub(r'https?://\S+|\S+@\S+|(?:\d{1,3}\.){3}\d{1,3}|[A-Za-z]:[\\/]\S+|/\S+', '[redacted]', message)
    tokens=re.findall(r'[A-Za-z][A-Za-z0-9_-]*|[0-9]+|[.,:;!?()]',message)
    kept=[];meaningful=False
    for word in tokens[:128]:
        if word.lower() in ERROR_MESSAGE_WORDS:
            kept.append(word);meaningful=True
        elif word in '.,:;!?()':
            kept.append(word)
        elif not kept or kept[-1]!='[redacted]':
            kept.append('[redacted]')
    return ' '.join(kept)[:512] if meaningful else None


def safe_api_error(raw, secrets=()):
    """Allow known fields/codes and redacted protocol vocabulary, never raw bodies."""
    summary = {'response_format': 'too_large' if len(raw) > 65536 else 'non_json',
               'validation_fields': [], 'validation_codes': []}
    if len(raw) > 65536:
        return summary
    try:
        data = parse_json(raw)
    except (ValueError, UnicodeError, RecursionError):
        return summary
    summary['response_format'] = 'json_object' if isinstance(data, dict) else 'json_other'
    if not isinstance(data, dict):
        return summary
    fields, codes = set(), set()
    hints = set()
    messages = set()

    def field(value):
        if not isinstance(value, str):
            return
        match = re.fullmatch(r'(?:metadata\.)?([A-Za-z]+)(?:\[[0-9]{1,6}\])?', value, re.IGNORECASE)
        aliases: dict[str, str] = {name.lower(): name for name in ERROR_FIELDS}
        if match and match[1].lower() in aliases:
            fields.add(aliases[match[1].lower()])

    def entry(value):
        if not isinstance(value, dict):
            return
        field(value.get('field'))
        for key in ('message','errorMessage','Message','ErrorMessage'):
            safe=diagnostic_message(value.get(key),secrets)
            if safe and len(messages)<8: messages.add(safe)
        code = value.get('code')
        if isinstance(code, str) and code in ERROR_CODES:
            codes.add(code)

    # Only known containers/keys are traversed. A small integer in a dedicated
    # errorCode field is a protocol code, not an arbitrary numeric response value.
    def known_error(value, depth=0):
        if not isinstance(value, dict) or depth > 3:
            return
        for key in ('errorCode', 'ErrorCode'):
            code = value.get(key)
            if type(code) is int and 0 <= code <= 9999:
                summary['error_code'] = code
        for key in ('errorMessage', 'ErrorMessage', 'message', 'Message'):
            message = value.get(key)
            if isinstance(message, str):
                safe = diagnostic_message(message, secrets)
                if safe and len(messages)<8: messages.add(safe)
                # Email/domain/URL suffixes such as .invalid must not be
                # mistaken for a server validation sentence.
                message = re.sub(r'\S+@\S+|https?://\S+', '', message.lower())
                for category, pattern in MESSAGE_HINTS.items():
                    if pattern.search(message):
                        hints.add(category)
        for key in ('error', 'Error', 'details', 'Details'):
            known_error(value.get(key), depth + 1)

    entry(data)
    known_error(data)
    for key in ('errors', 'validationErrors', 'ModelState'):
        errors = data.get(key)
        if isinstance(errors, dict):
            for name, values in errors.items():
                field(name)
                if isinstance(values, list):
                    for value in values:
                        entry(value)
                else:
                    entry(values)
        elif isinstance(errors, list):
            for value in errors:
                entry(value)
    summary.update(validation_fields=sorted(fields), validation_codes=sorted(codes))
    if messages:
        summary['diagnostic_messages'] = sorted(messages)
        summary['message_values_redacted'] = True
    if hints:
        # These fixed labels are text-derived hints, not claimed official codes.
        summary['message_hints'] = sorted(hints)
    return summary


def read_error_summary(response, secrets=()):
    try:
        return safe_api_error(response.read(65537), secrets)
    except (OSError, http.client.HTTPException):
        return {'response_format': 'read_failed', 'validation_fields': [], 'validation_codes': []}
