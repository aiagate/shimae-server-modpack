"""Check declared NeoForge MOD version conflicts from a fixed-file metadata lock.

Only read ZIP metadata. Never launch Minecraft or load classes from MOD JARs.
"""
import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tomllib
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from zipfile import BadZipFile, ZipFile

import pack_io
import pack_validation

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'ci' / 'mod-dependencies.json'
TOML = 'META-INF/neoforge.mods.toml'
MANIFEST = 'META-INF/MANIFEST.MF'
JARJAR = 'META-INF/jarjar/metadata.json'
LIBS = {
    'maven-artifact-3.8.5.jar': '91172bc294d6eab02fc9f45f4ea01fd0e418962d128cf489abea7b6957d988ee',
    'commons-lang3-3.14.0.jar': '7b96bf3ee68949abb5bc465559ac270e0551596fa34523fddf890ec418dde13c',
}


def read_entry(archive, name, limit=2 * 1024**2):
    info = archive.getinfo(name)
    if info.file_size > limit:
        raise ValueError(f'Oversized archive entry: {name}')
    return archive.read(info)


def implementation_version(archive, names):
    if MANIFEST not in names:
        return '0.0NONE'
    # Only the main manifest section counts; continuation lines start with space.
    manifest = read_entry(archive, MANIFEST).replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    main = manifest.split(b'\n\n', 1)[0].replace(b'\n ', b'')
    return next((line.partition(b': ')[2].decode('utf-8') for line in main.split(b'\n')
                 if line.lower().startswith(b'implementation-version: ')), '0.0NONE')


def inspect_jar(stream, nested=False, depth=0, jarjar=None):
    if depth > 8:
        raise ValueError('Nested JAR depth exceeds limit')
    with ZipFile(stream) as archive:
        names = set(archive.namelist())
        mods = []
        if TOML in names:
            data = tomllib.loads(read_entry(archive, TOML).decode('utf-8-sig'))
            for mod in data['mods']:
                mod_id = mod['modId']
                version = mod.get('version', '1').replace('${file.jarVersion}', implementation_version(archive, names))
                if not re.fullmatch(r'[0-9][^\r\n\t$]*', version):
                    raise ValueError(f'Unresolved version for {mod_id}: {version!r}')
                dependencies = []
                for item in data.get('dependencies', {}).get(mod_id, []):
                    kind = item.get('type', 'required').lower()
                    side = item.get('side', 'BOTH').lower()
                    if kind not in {'required', 'optional', 'incompatible', 'discouraged'} or side not in {'client', 'server', 'both'}:
                        raise ValueError(f'Unknown dependency type or side for {mod_id}')
                    # FML uses a single space for an omitted, unbounded range.
                    dependencies.append([item['modId'], kind, side, item.get('versionRange', ' ')])
                mods.append({'id': mod_id, 'version': version, 'nested': nested, 'deps': dependencies,
                             **({'jarjar': jarjar} if jarjar else {})})
        elif not nested:
            raise ValueError(f'Missing {TOML} in pinned JAR')
        if JARJAR in names:
            entries = json.loads(read_entry(archive, JARJAR))['jars']
            for entry in entries:
                path = entry['path']
                identifier = entry.get('identifier')
                version = entry.get('version')
                metadata = None
                if identifier and version:
                    metadata = {
                        'coordinate': f"{identifier['group']}:{identifier['artifact']}",
                        'range': version['range'],
                        'artifact_version': version['artifactVersion'],
                    }
                mods.extend(inspect_jar(io.BytesIO(read_entry(archive, path, 128 * 1024**2)),
                                        True, depth + 1, metadata))
        return mods


@dataclass(frozen=True)
class Check:
    owner: str
    owner_version: str
    target: str
    version: str
    version_range: str
    kind: str


def dependency_checks(side, mods):
    """Check constraints on top-level mods; nested candidates can provide targets."""
    versions = defaultdict(set)
    for mod in mods:
        versions[mod['id']].add(mod['version'])
    checks, unresolved = [], []
    for mod in mods:
        if mod['nested']:
            continue  # A bundled candidate's constraints need not be active.
        for target, kind, applies, spec in mod['deps']:
            if kind == 'discouraged' or applies not in ('both', side):
                continue
            present = versions.get(target, set())
            checks.extend(Check(mod['id'], mod['version'], target, version, spec, kind)
                          for version in sorted(present))
            if not present and kind == 'required':
                unresolved.append(f'{mod["id"]} -> {target}: no statically known provider')
    return checks, sorted(set(unresolved))


def exclude_ineligible_bundles(mods, java, libs, minecraft):
    """Narrow competing providers only when their Jar-in-Jar ranges identify one version."""
    providers = defaultdict(list)
    for mod in mods:
        providers[mod['id']].append(mod)

    excluded = set()
    for mod_id, candidates in providers.items():
        if len({mod['version'] for mod in candidates}) < 2:
            continue
        metadata = [mod.get('jarjar') for mod in candidates]
        if any(not entry for entry in metadata) or len({entry['coordinate'] for entry in metadata}) != 1:
            continue
        coordinate = metadata[0]['coordinate']
        artifact_versions = {entry['artifact_version'] for entry in metadata}
        ranges = {entry['range'] for entry in metadata}
        if any(not spec.startswith(('[', '(')) for spec in ranges):
            continue
        checks = [Check(mod_id, '', coordinate, version, spec, 'required')
                  for version in artifact_versions for spec in ranges]
        eligible = artifact_versions - {check.version for check in compare(checks, java, libs, minecraft)}
        if len(eligible) == 1:
            selected_versions = {mod['version'] for mod in candidates
                                 if mod['jarjar']['artifact_version'] in eligible}
            excluded.update((mod_id, mod['version']) for mod in candidates
                            if mod['version'] not in selected_versions)
    return [mod for mod in mods if (mod['id'], mod['version']) not in excluded]


def compare(checks, java, libs, minecraft):
    for jar, sha in LIBS.items():
        with (libs / jar).open('rb') as file:
            if hashlib.file_digest(file, 'sha256').hexdigest() != sha:
                raise ValueError(f'Unexpected {jar} SHA-256')
    pairs = sorted({(c.version_range, c.target, c.version) for c in checks})
    if any(any(char in x for char in '\r\n\t') for row in pairs for x in row):
        raise ValueError('Unexpected control characters in mod metadata')
    classpath = os.pathsep.join(str(libs / jar) for jar in LIBS)
    result = subprocess.run([java, '-cp', classpath, str(ROOT / 'scripts/NeoForgeVersionRanges.java'), minecraft],
                            input=''.join('\t'.join(row) + '\n' for row in pairs), encoding='utf-8',
                            stdout=subprocess.PIPE, timeout=60, check=True)
    results = result.stdout.splitlines()
    if len(results) != len(pairs) or set(results) - {'yes', 'no'}:
        raise ValueError('Invalid Maven range-check output')
    matches = dict(zip(pairs, results, strict=True))
    return [check for check in checks
            if (matches[(check.version_range, check.target, check.version)] == 'yes') == (check.kind == 'incompatible')]


def read_pack():
    pack = ROOT / 'pack'
    meta = pack_validation.parse_json((pack / 'release.json').read_bytes())
    refs = {side: pack_io.reference_map(pack_validation.parse_json((pack / f'{side}.refs.json').read_bytes())['files'])
            for side in pack_io.KINDS}
    return meta, {side: [f'{pid}-{r["fileID"]}' for pid, r in sorted(rows.items())] for side, rows in refs.items()}


def refresh_lock(pins, existing, directory):
    if not directory.is_dir():
        raise ValueError(f'Not an archive directory: {directory}')
    updated = {}
    for pin in sorted(set(pins)):
        paths = [p for suffix in ('.jar', '.zip') if (p := directory / (pin + suffix)).is_file()]
        if len(paths) == 0 and pin in existing:
            updated[pin] = existing[pin]
            continue
        if len(paths) != 1:
            raise ValueError(f'Provide exactly one fixed archive for {pin}: {pin}.jar or {pin}.zip')
        path = paths[0]
        try:
            with path.open('rb') as stream:
                sha = hashlib.file_digest(stream, 'sha256').hexdigest()
                stream.seek(0)
                if path.suffix == '.jar':
                    mods = inspect_jar(stream)
                    if not mods:
                        raise ValueError('No NeoForge mod IDs in archive')
                else:
                    with ZipFile(stream) as archive:
                        if TOML in archive.namelist() or not any(n.startswith('shaders/') for n in archive.namelist()):
                            raise ValueError('Non-MOD ZIP must be an identified shader pack')
                    mods = []
            entry = {'sha256': sha, 'kind': 'mod' if mods else 'shader', 'mods': mods}
            if pin in existing and existing[pin]['sha256'] != sha:
                raise ValueError('Archive bytes changed for an existing fixed file ID')
            updated[pin] = entry
        except (ValueError, OSError, KeyError, BadZipFile) as exc:
            raise ValueError(f'{path.name}: {exc}') from exc
    return updated


def write_lock(records):
    # One line per pin so updating one MOD creates a bounded, reviewable diff.
    rows = [f'  {json.dumps(pin)}: {json.dumps(entry, ensure_ascii=True)}' for pin, entry in records.items()]
    text = '{\n' + ',\n'.join(rows) + '\n}\n'
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(text, encoding='utf-8')


def run_lint(meta, refs, records, java, libs):
    wanted = set().union(*map(set, refs.values()))
    missing, stale = wanted - records.keys(), records.keys() - wanted
    if missing or stale:
        raise ValueError(f'Metadata lock differs from refs; missing={sorted(missing)}, stale={sorted(stale)}. Update with --refresh.')
    for pin, record in records.items():
        if (not re.fullmatch(r'[0-9a-f]{64}', record['sha256']) or record['kind'] not in {'mod', 'shader'}
                or bool(record['mods']) != (record['kind'] == 'mod')):
            raise ValueError(f'Invalid metadata for {pin}')
    mc = meta['minecraft_version']
    if not meta['loader_id'].startswith('neoforge-'):
        raise ValueError('Dependency lint expects a NeoForge pack')
    loader = meta['loader_id'].removeprefix('neoforge-')
    system = [{'id': k, 'version': v, 'nested': False, 'deps': []}
              for k, v in [('minecraft', mc), ('neoforge', loader)]]
    checks_by_side, unresolved_by_side = {}, {}
    for side, pins in refs.items():
        mods = [m for pin in pins for m in records[pin]['mods']]
        eligible_mods = exclude_ineligible_bundles(mods, java, libs, mc)
        checks, unresolved = dependency_checks(side, system + eligible_mods)
        checks_by_side[side] = checks
        unresolved_by_side[side] = unresolved
    conflicts = set(compare([c for checks in checks_by_side.values() for c in checks], java, libs, mc))
    found = False
    for side, checks in checks_by_side.items():
        groups = defaultdict(set)
        for check in checks:
            key = (check.owner, check.owner_version, check.target, check.version_range, check.kind)
            groups[key].add(check)
        unresolved = unresolved_by_side[side]
        for (owner, owner_version, target, spec, kind), candidates in groups.items():
            failed = candidates & conflicts
            if not failed:
                continue
            versions = ', '.join(sorted(c.version for c in candidates))
            action = 'conflicts with' if kind == 'incompatible' else 'requires'
            actual = 'candidate versions' if len(candidates) > 1 else 'installed'
            problem = f'{owner} {owner_version} {action} {target} {spec!r} ({kind}); {actual} {versions}'
            if failed == candidates:
                found = True
                print(f'[{side}] {problem}', file=sys.stderr)
            else:
                unresolved.append(f'{problem} (some candidates violate the constraint)')
        for warning in unresolved:
            print(f'[{side}] not resolved by static version lint: {warning}')
        print(f'[{side}] {len(refs[side])} fixed files, {len(groups)} version constraints, {len(unresolved)} unresolved')
    return int(found)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--refresh', type=Path, metavar='ARCHIVE_DIR')
    modes.add_argument('--libs', type=Path, metavar='MAVEN_LIB_DIR')
    parser.add_argument('--java', default=os.environ.get('JAVA', 'java'))
    args = parser.parse_args()
    try:
        meta, refs = read_pack()
        records = pack_validation.parse_json(LOCK.read_bytes()) if LOCK.is_file() else {}
        if args.refresh is not None:
            write_lock(refresh_lock(refs['client'], records, args.refresh))
            return 0
        return run_lint(meta, refs, records, args.java, args.libs)
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f'Dependency lint: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
