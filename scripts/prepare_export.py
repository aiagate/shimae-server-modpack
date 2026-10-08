"""Prepare a reviewed App-origin copy without modifying manifest or live settings."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

from release import Invalid, MAX_ZIP, need, parse_json, validate
from verify_app_exports import UNWANTED

ADDITIONS = {'overrides/LICENSE-Shimae.txt': 'LICENSE',
             'overrides/THIRD-PARTY-NOTICES.txt': 'LICENSE-SCOPE.txt'}


def prepare(blob, plan, config, root):
    sha = lambda content: hashlib.sha256(content).hexdigest()
    need(sha(blob) == plan.get('source_sha256'), 'original differs from reviewed preparation source')
    need(plan.get('additions') == ADDITIONS and isinstance(plan.get('omit_paths'), list) and
         len(plan['omit_paths']) == len(set(plan['omit_paths'])), 'invalid preparation plan')
    need(all(isinstance(n, str) and n.startswith('overrides/config/') and UNWANTED.search(n)
             for n in plan['omit_paths']), 'only reviewed personal/unused state may be omitted')
    validate(blob, dict(config, reviewed_sha256=sha(blob)))
    output = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(blob)) as source:
        names = set(source.namelist())
        need(set(plan['omit_paths']) <= names, 'reviewed removal path missing')
        need(sha(source.read('manifest.json')) == plan.get('manifest_sha256') and
             sha(source.read('modlist.html')) == plan.get('modlist_sha256'), 'App manifest/modlist source mismatch')
        with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as dest:
            for name in sorted(names - set(plan['omit_paths'])):
                if name.endswith('/'):
                    continue
                info = zipfile.ZipInfo(name, date_time=(2000, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                dest.writestr(info, source.read(name), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            for name, path in sorted(ADDITIONS.items()):
                need(name not in names, 'license addition would overwrite source')
                info = zipfile.ZipInfo(name, date_time=(2000, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                dest.writestr(info, (root / path).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    result = output.getvalue()
    validate(result, dict(config, reviewed_sha256=sha(result)))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--plan', type=Path, default=Path('exports/preparation.json'))
    parser.add_argument('--config', type=Path, default=Path('release.json'))
    args = parser.parse_args()
    try:
        need(args.source.is_file() and not args.source.is_symlink() and
             args.output.suffix == '.zip' and not args.output.exists() and
             not args.output.is_symlink(), 'use a regular source and a new output ZIP')
        with args.source.open('rb') as handle:
            blob = handle.read(MAX_ZIP + 1)
        result = prepare(blob, parse_json(args.plan.read_bytes()), parse_json(args.config.read_bytes()), Path.cwd())
        with args.output.open('xb') as handle:
            handle.write(result)
        print('Reviewed copy prepared; manifest, modlist and retained configuration bytes unchanged.')
        return 0
    except (Invalid, OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, RuntimeError):
        print('STOP: export preparation failed; original unchanged; no upload performed.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
