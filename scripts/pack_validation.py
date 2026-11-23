"""Validate modpack configuration, manifests, and ZIP contents."""
import hashlib
import html
import io
import json
import re
import stat
import zipfile
from pathlib import Path

MAX_ZIP = 90 * 1024 * 1024  # Repository policy, not a CurseForge API limit.
MAX_TOTAL = 256 * 1024 * 1024
MAX_ENTRY = 32 * 1024 * 1024
MAX_ENTRIES = 10000
REVIEWED_COMMENTS_PATH = Path(__file__).with_name('reviewed_comments.json')
DENIED = {'saves', 'world', 'worlds', 'logs', 'crash-reports', 'screenshots',
          'backups', 'options.txt', 'optionsof.txt', 'servers.dat', 'servers.dat_old',
          'server.properties', 'whitelist.json', 'ops.json', 'usercache.json',
          'secrets', 'credentials', 'session.lock', 'level.dat', 'playerdata'}
SENSITIVE = re.compile(rb'(?i)(-----BEGIN [A-Z ]*PRIVATE KEY|'
                       rb'(?:password|passwd|token|api[_-]?key|secret)\s*["\x27]?\s*[:=]\s*["\x27]?[^\s"\x27,}]{4,}|'
                       rb'https?://|(?:\d{1,3}\.){3}\d{1,3}|'
                       rb'(?:localhost|[a-z0-9.-]+\.(?:local|lan|internal))\b)')
PUBLIC_MODLIST_URL = re.compile(
    rb'https?://(?:(?:www|minecraft)\.)?curseforge\.com/'
    rb'(?:minecraft/(?:mc-mods|shaders)/[a-z0-9-]+(?:/files/[0-9]+)?|projects/[a-z0-9-]+)/?'
    rb'(?=[\s"\x27<>]|$)', re.IGNORECASE)


class Invalid(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise Invalid(message)


def positive(value):
    return type(value) is int and value > 0


def parse_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, 'JSON has duplicate keys')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique)


def config_check(config):
    need(isinstance(config, dict), 'config must be an object')
    need(set(config) == {'project_id', 'minecraft_version', 'loader_id',
                        'game_version_names', 'release_type', 'display_name',
                        'reviewed_sha256'}, 'invalid runtime validation config keys')
    need(positive(config['project_id']), 'project_id is not configured')
    for key in ('minecraft_version', 'loader_id', 'display_name'):
        need(isinstance(config[key], str) and config[key].strip() and
             'REPLACE' not in config[key] and len(config[key]) < 200,
             key + ' is not configured')
    need(config['release_type'] in ('alpha', 'beta', 'release'), 'invalid release_type')
    names = config['game_version_names']
    need(isinstance(names, list) and len(names) == 3 and
         all(isinstance(n, str) for n in names), 'set exactly Minecraft, loader, Client game version names')
    family = config['loader_id'].split('-')[0]
    loader_name = {'forge': 'Forge', 'neoforge': 'NeoForge', 'fabric': 'Fabric',
                   'quilt': 'Quilt'}.get(family)
    need(loader_name is not None and config['loader_id'].startswith(family + '-'), 'unsupported loader ID')
    need(set(names) == {config['minecraft_version'], loader_name, 'Client'},
         'game_version_names must match Minecraft version, loader and Client')
    need(isinstance(config['reviewed_sha256'], str) and
         re.fullmatch('[0-9a-f]{64}', config['reviewed_sha256']),
         'reviewed_sha256 must identify the verified client ZIP')


def checked_override(content, name):
    """Do not skip comments generically; exempt only reviewed exact comment lines."""
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        raise Invalid('binary overrides require a separately reviewed policy') from None
    need(b'\x00' not in content, 'override contains a possible credential or connection destination')
    # Credential detection applies even to an approved documentation comment.
    credentials = re.compile(rb'(?i)(-----BEGIN [A-Z ]*PRIVATE KEY|'
        rb'(?:password|passwd|token|api[_-]?key|secret)\s*["\x27]?\s*[:=]\s*["\x27]?[^\s"\x27,}]{4,})')
    need(not credentials.search(content), 'override contains a possible credential')
    policy = parse_json(REVIEWED_COMMENTS_PATH.read_bytes())
    approved = policy.get(name, [])
    for line in text.splitlines():
        raw = line.strip().encode('utf-8')
        reviewed = raw.startswith(b'#') and hashlib.sha256(raw).hexdigest() in approved
        need(reviewed or not SENSITIVE.search(raw),
             'override contains a possible credential or connection destination')


def validate(blob, config):
    config_check(config)
    need(len(blob) <= MAX_ZIP, 'ZIP exceeds 90 MiB repository limit')
    digest = hashlib.sha256(blob).hexdigest()
    need(digest == config['reviewed_sha256'], 'ZIP differs from reviewed_sha256')
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        entries = archive.infolist()
        need(0 < len(entries) <= MAX_ENTRIES, 'invalid ZIP entry count')
        need(sum(e.file_size for e in entries) <= MAX_TOTAL, 'expanded ZIP exceeds 256 MiB')
        seen = set()
        manifest = None
        for entry in entries:
            name = entry.filename
            parts = name.rstrip('/').split('/')
            need(name == entry.orig_filename and '\\' not in name and ':' not in name and
                 all(p not in ('', '.', '..') for p in parts) and
                 all(ord(c) >= 32 and ord(c) != 127 for c in name), 'unsafe ZIP path')
            normalized = name.rstrip('/').casefold()
            need(normalized not in seen, 'duplicate ZIP path')
            seen.add(normalized)
            mode = entry.external_attr >> 16
            need(stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR), 'special ZIP entry')
            need(not entry.flag_bits & 1, 'encrypted ZIP entry')
            need(entry.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED), 'unsupported ZIP compression')
            need(entry.file_size <= MAX_ENTRY and
                 entry.file_size <= max(entry.compress_size, 1) * 200, 'ZIP entry size/ratio limit')
            need(parts[0] == 'overrides' or name in ('manifest.json', 'modlist.html'),
                 'ZIP must have manifest.json, optional modlist.html, and overrides only')
            lower = [p.casefold() for p in parts]
            need(not any(p in DENIED or p.startswith('.') or
                         p.endswith(('.pem', '.key', '.log', '.mca', '.jar', '.zip', '.7z'))
                         for p in lower), 'private/runtime/binary archive content is forbidden')
            if entry.is_dir():
                need(entry.file_size == 0, 'nonempty ZIP directory')
                continue
            need(name != 'overrides', 'overrides must be a directory')
            content = archive.read(entry)  # Verify CRC; never extract.
            if name == 'manifest.json':
                need(len(content) <= 2 * 1024 * 1024, 'manifest too large')
                manifest = parse_json(content)
                # Inspect normalized JSON so escaped keys/values cannot bypass scans.
                canonical = json.dumps(manifest, ensure_ascii=False).encode('utf-8')
                need(not SENSITIVE.search(canonical),
                     'manifest contains a possible credential or connection destination')
            elif name == 'modlist.html':
                try:
                    text = html.unescape(content.decode('utf-8')).encode('utf-8')
                except UnicodeDecodeError:
                    raise Invalid('modlist.html must be UTF-8 text') from None
                # App mod lists contain public project links; no arbitrary URL exemption.
                inspected = PUBLIC_MODLIST_URL.sub(b'', text)
                need(b'\x00' not in text and not SENSITIVE.search(inspected),
                     'modlist contains a possible credential or connection destination')
            elif parts[0] == 'overrides':
                checked_override(content, name)
        if not isinstance(manifest, dict):
            raise Invalid('root manifest.json missing or invalid')
        need(any(e.filename == 'overrides/' and e.is_dir() or
                 e.filename.startswith('overrides/') and len(e.filename) > len('overrides/')
                 for e in entries), 'overrides directory missing')
        need(manifest.get('manifestType') == 'minecraftModpack' and
             type(manifest.get('manifestVersion')) is int and manifest['manifestVersion'] == 1,
             'unsupported manifest format')
        need(manifest.get('overrides') == 'overrides', 'unsupported overrides directory')
        for field in ('name', 'version'):
            need(isinstance(manifest.get(field), str) and manifest[field].strip(), 'manifest identity missing')
        # App exports may contain an empty author; attribution is confirmed
        # separately. Do not rewrite the generated manifest to satisfy our checker.
        need(isinstance(manifest.get('author'), str), 'manifest author must be a string')
        need(not manifest['version'].startswith('0.0.0-local.') and
             all('REPLACE' not in manifest[field] for field in ('name', 'version', 'author')),
             'local reconstruction draft or placeholder identity cannot be submitted')
        minecraft = manifest.get('minecraft')
        if not isinstance(minecraft, dict) or minecraft.get('version') != config['minecraft_version']:
            raise Invalid('Minecraft version differs from export')
        loaders = minecraft.get('modLoaders')
        need(isinstance(loaders, list) and len(loaders) == 1 and isinstance(loaders[0], dict) and
             loaders[0].get('id') == config['loader_id'] and loaders[0].get('primary') is True,
             'loader differs from export (one primary loader required)')
        files = manifest.get('files')
        if not isinstance(files, list) or not files:
            raise Invalid('manifest files must be a nonempty list')
        ids = set()
        for item in files:
            need(isinstance(item, dict) and positive(item.get('projectID')) and
                 positive(item.get('fileID')) and type(item.get('required')) is bool,
                 'invalid manifest file reference')
            need(item['projectID'] not in ids, 'duplicate project reference')
            ids.add(item['projectID'])
    return digest
