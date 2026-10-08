"""Check human-confirmed App exports; never generate or modify ZIP contents."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tomllib
import zipfile

import fetch_export
from release import Invalid, MAX_ZIP, config_check, need, parse_json, positive, validate

KINDS = ('client', 'server')
HEX = re.compile(r'[0-9a-f]{64}')
FILENAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9_. -]{0,180}\.zip')
UNWANTED = re.compile(r'(?i)(?:/benchmarks?/|/chunky/(?:tasks/|[^/]+\.(?:csv|properties)$)|sodium-fingerprint\.json$|'
                      r'bonsaitrees4|/tfc(?:-|\.)|/tfcoffsetsmoker|\.bak(?:\.|$))')


class InputWait(Invalid):
    """Untouched, human-confirmed App exports have not been supplied yet."""


def reference_map(files):
    need(isinstance(files, list) and files, 'reference lock must contain files')
    result = {}
    for item in files:
        need(isinstance(item, dict) and set(item) <= {'projectID', 'fileID', 'required', 'isLocked'}
             and positive(item.get('projectID')) and positive(item.get('fileID'))
             and type(item.get('required')) is bool
             and ('isLocked' not in item or type(item['isLocked']) is bool),
             'invalid locked MOD reference')
        need(item['projectID'] not in result, 'duplicate locked MOD reference')
        result[item['projectID']] = item
    return result


def policy_check(policy, refs):
    need(isinstance(policy, dict) and policy.get('schema_version') == 1, 'invalid policy')
    for key in ('forbidden_project_ids', 'retained_project_ids', 'client_only_project_ids'):
        values = policy.get(key)
        need(isinstance(values, list) and all(positive(v) for v in values)
             and len(values) == len(set(values)), 'invalid policy IDs')
    counts = policy.get('expected_counts')
    need(isinstance(counts, dict) and set(counts) == set(KINDS), 'invalid expected counts')
    for kind in KINDS:
        need(positive(counts[kind]) and len(refs[kind]) == counts[kind], 'reference count mismatch')
        need(not set(refs[kind]) & set(policy['forbidden_project_ids']), 'forbidden MOD reference')
        need(set(policy['retained_project_ids']) <= set(refs[kind]), 'required retained MOD missing')
    need(set(refs['server']) <= set(refs['client']), 'server must be a client subset')
    need(set(refs['client']) - set(refs['server']) == set(policy['client_only_project_ids']),
         'client-only MOD difference mismatch')
    need(all(v == refs['client'][k] for k, v in refs['server'].items()),
         'shared MOD reference differs')
    hashes = policy.get('override_sha256')
    need(isinstance(hashes, dict) and set(hashes) == set(KINDS), 'invalid override policy')
    for kind in KINDS:
        need(isinstance(hashes[kind], dict) and hashes[kind], 'override review is required')
        for name, digest in hashes[kind].items():
            need(isinstance(name, str) and name.startswith('overrides/') and
                 '..' not in name.split('/') and not UNWANTED.search(name) and
                 isinstance(digest, str) and HEX.fullmatch(digest), 'invalid override policy entry')
    common = set(hashes['client']) & set(hashes['server'])
    need(all(hashes['client'][n] == hashes['server'][n] for n in common),
         'shared override policy differs')
    need(isinstance(policy.get('commented_json_paths'), list) and
         all(isinstance(n, str) for n in policy['commented_json_paths']), 'invalid JSON comment policy')


def load_inputs(lock_path, policy_path, config_path, *, require_assets=True):
    lock = parse_json(lock_path.read_bytes())
    policy = parse_json(policy_path.read_bytes())
    config = parse_json(config_path.read_bytes())
    need(isinstance(lock, dict) and lock.get('schema_version') == 1 and
         lock.get('repository') == fetch_export.REPOSITORY, 'invalid export lock repository/schema')
    need(isinstance(config, dict) and positive(config.get('project_id')), 'project_id is not configured')
    profiles = lock.get('profiles')
    need(isinstance(profiles, dict) and set(profiles) == set(KINDS), 'two App profiles are required')
    refs = {}
    for kind in KINDS:
        item = profiles[kind]
        need(isinstance(item, dict) and item.get('reference_lock') == f'exports/{kind}.refs.json',
             'use the fixed profile reference lock path')
        source = parse_json((lock_path.parent / f'{kind}.refs.json').read_bytes())
        need(isinstance(source, dict), 'invalid reference lock')
        refs[kind] = reference_map(source.get('files'))
    policy_check(policy, refs)
    # Provenance is a human assertion, not something ZIP format or SHA can prove.
    for kind in KINDS:
        origin = profiles[kind].get('origin')
        need(isinstance(origin, dict) and origin.get('exporter') == 'CurseForge App',
             'App export origin record is required')
        if origin.get('confirmed') is not True:
            raise InputWait('untouched App exports and human provenance confirmation are pending')
        for field in ('confirmed_by', 'exported_at', 'source_profile'):
            need(isinstance(origin.get(field), str) and origin[field].strip() and
                 'REPLACE' not in origin[field], 'complete the human App export origin record')
    need(isinstance(lock.get('version'), str) and lock['version'].strip() and
         'REPLACE' not in lock['version'], 'App export version is not configured')
    configs = {}
    for kind in KINDS:
        item = profiles[kind]
        if require_assets and item.get('asset_id') is None:
            raise InputWait('reviewed public Release asset IDs are pending')
        need((positive(item.get('asset_id')) or not require_assets and item.get('asset_id') is None)
             and positive(item.get('size_bytes')) and
             item['size_bytes'] <= MAX_ZIP and isinstance(item.get('filename'), str) and
             FILENAME.fullmatch(item['filename']) and lock['version'] in item['filename'] and
             isinstance(item.get('sha256'), str) and HEX.fullmatch(item['sha256']),
             'complete reviewed asset ID/name/size/SHA for each App export')
        need(isinstance(item.get('manifest_name'), str) and item['manifest_name'].strip() and
             'REPLACE' not in item['manifest_name'], 'App manifest name is not configured')
        configs[kind] = dict(config, export_asset_id=item['asset_id'], reviewed_sha256=item['sha256'])
        config_check(configs[kind])
    need((profiles['client']['asset_id'] is None or profiles['server']['asset_id'] is None or
          profiles['client']['asset_id'] != profiles['server']['asset_id']) and
         profiles['client']['filename'].casefold() != profiles['server']['filename'].casefold(),
         'use distinct client/server assets and names')
    config_check(config)
    need(config['export_asset_id'] == profiles['client']['asset_id'] and
         config['reviewed_sha256'] == profiles['client']['sha256'], 'release config/client lock differ')
    need(config['minecraft_version'] == lock.get('minecraft_version') and
         config['loader_id'] == lock.get('mod_loader'), 'release config/locked game versions differ')
    return lock, policy, refs, configs


def check_blob(blob, kind, lock, policy, refs, config):
    item = lock['profiles'][kind]
    need(len(blob) == item['size_bytes'], 'App export size differs from lock')
    digest = validate(blob, config)  # CRC, bounds, paths, manifest, exact SHA, privacy.
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        manifest = parse_json(archive.read('manifest.json'))
        need(manifest['name'] == item['manifest_name'] and manifest['version'] == lock['version'],
             'App manifest identity differs from lock')
        need(reference_map(manifest['files']) == refs[kind], 'App MOD references differ from lock')
        hashes = {}
        for entry in archive.infolist():
            need(not (entry.external_attr >> 16) & 0o111 or entry.is_dir(), 'executable ZIP file')
            if entry.is_dir() or not entry.filename.startswith('overrides/'):
                continue
            name = entry.filename
            need(not UNWANTED.search(name), 'unnecessary personal/removed MOD state in App export')
            content = archive.read(entry)
            need(not re.search(rb'(?i)\b(?:tfc|tfcoffsetsmoker):', content), 'removed MOD namespace in config')
            if name.endswith('.toml'):
                tomllib.loads(content.decode('utf-8'))
            elif name.endswith('.json') and name not in policy['commented_json_paths']:
                parse_json(content)
            hashes[name] = hashlib.sha256(content).hexdigest()
        need(hashes == policy['override_sha256'][kind], 'override content differs from reviewed policy')
    return digest


def read_blob(path):
    need(path.is_file() and not path.is_symlink() and path.suffix == '.zip', 'use a regular App export ZIP')
    with path.open('rb') as handle:
        return handle.read(MAX_ZIP + 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', type=Path, default=Path('exports/exports.lock.json'))
    parser.add_argument('--policy', type=Path, default=Path('exports/policy.json'))
    parser.add_argument('--release-config', type=Path, default=Path('release.json'))
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check-state', action='store_true')
    mode.add_argument('--fetch', action='store_true')
    mode.add_argument('--directory', type=Path)
    mode.add_argument('--client', type=Path, help='local original client export; also needs --server')
    parser.add_argument('--server', type=Path)
    parser.add_argument('--profile', choices=KINDS)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--commit')
    parser.add_argument('--github-output', type=Path)
    args = parser.parse_args()
    try:
        try:
            lock, policy, refs, configs = load_inputs(args.lock, args.policy, args.release_config,
                                                     require_assets=not bool(args.client))
        except InputWait:
            if not args.check_state:
                raise
            print('INPUT_WAIT: untouched App exports are pending; no assets checked or submitted.')
            if args.github_output:
                with args.github_output.open('a') as handle:
                    handle.write('ready=false\n')
            return 0
        if args.check_state:
            print('App input records are configured; ZIP contents still require verification.')
            if args.github_output:
                with args.github_output.open('a') as handle:
                    handle.write('ready=true\n')
            return 0
        need(not args.server or args.client, '--server requires --client')
        need(not args.client or args.server, 'both local App exports are required')
        need(not args.profile or args.directory, '--profile is for submission artifact recheck only')
        need(not args.fetch or args.output, '--fetch requires a new output directory')
        kinds = (args.profile,) if args.profile else KINDS
        blobs, paths = {}, {}
        for kind in kinds:
            item = lock['profiles'][kind]
            if args.fetch:
                blob = fetch_export.fetch(configs[kind], expected_name=item['filename'],
                                          expected_size=item['size_bytes'])
            else:
                source = args.directory / item['filename'] if args.directory else getattr(args, kind)
                blob = read_blob(source)
                paths[kind] = source.resolve()
            check_blob(blob, kind, lock, policy, refs, configs[kind])
            blobs[kind] = blob
        if args.output:
            need(isinstance(args.commit, str) and re.fullmatch(r'[0-9a-f]{40}', args.commit),
                 'saved receipt requires a source commit SHA')
            args.output.mkdir(parents=True, exist_ok=False)
            for kind, blob in blobs.items():
                path = args.output / lock['profiles'][kind]['filename']
                with path.open('xb') as handle:
                    handle.write(blob)  # Original bytes only; no ZIP reconstruction.
                need(read_blob(path) == blob, 'saved App export bytes changed')
                paths[kind] = path.resolve()
            receipt = {'commit': args.commit, 'lock_sha256': hashlib.sha256(args.lock.read_bytes()).hexdigest(),
                       'project_id': configs['client']['project_id'], 'version': lock['version'],
                       'status': 'validated', 'app_origin': 'human-confirmed; not machine-proven',
                       'exports': {k: {field: lock['profiles'][k][field]
                                      for field in ('asset_id', 'filename', 'size_bytes', 'sha256')}
                                   for k in kinds}}
            (args.output / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
            (args.output / 'SHA256SUMS').write_text(''.join(
                f"{lock['profiles'][k]['sha256']}  {lock['profiles'][k]['filename']}\n" for k in kinds))
        if args.github_output:
            with args.github_output.open('a') as handle:
                for kind, path in paths.items():
                    need(not any(ord(c) < 32 or ord(c) == 127 for c in str(path)), 'unsafe output path')
                    handle.write(f'{kind}_zip={path}\n')
        print('Verified unmodified App export bytes; no submission performed.')
        return 0
    except InputWait:
        print('INPUT_WAIT: provide two untouched App exports and confirm their origin before fetching or submitting.',
              file=sys.stderr)
        return 1
    except (Invalid, OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, RuntimeError,
            NotImplementedError):
        print('STOP: App export validation failed; no upload or submission performed.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
