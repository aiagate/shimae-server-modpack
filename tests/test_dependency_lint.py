from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import sys
import unittest
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import dependency_lint as lint


def jar(**entries):
    result = io.BytesIO()
    with ZipFile(result, 'w') as z:
        for name, content in entries.items():
            z.writestr(name, content)
    return result.getvalue()


def mod(mod_id, version, extra='', **entries: bytes):
    return jar(**{'META-INF/neoforge.mods.toml': f'[[mods]]\nmodId="{mod_id}"\nversion="{version}"\n{extra}', **entries})


class DependencyLintTest(unittest.TestCase):
    def test_installed_optional_dependency_is_checked_on_both_sides(self):
        clutter = mod('clutternomore', '3.1.3+1.21.1', '''
[[dependencies.clutternomore]]
modId="domum_ornamentum"
type="optional"
versionRange="[1.21.1-1.0.197-BETA,1.21.2)"
side="BOTH"
''')
        domum = mod('domum_ornamentum', '${file.jarVersion}', **{
            'META-INF/MANIFEST.MF': b'Manifest-Version: 1.0\r\nImplementation-Version: 1.0.\r\n 231\r\n\r\n',
        })
        mods = lint.inspect_jar(io.BytesIO(clutter)) + lint.inspect_jar(io.BytesIO(domum))
        for side in ('client', 'server'):
            with self.subTest(side=side):
                checks, errors = lint.dependency_checks(side, mods)
                self.assertEqual(errors, [])
                self.assertEqual(len(checks), 1)
                check = checks[0]
                self.assertEqual((check.owner, check.target, check.version, check.version_range), (
                    'clutternomore', 'domum_ornamentum', '1.0.231', '[1.21.1-1.0.197-BETA,1.21.2)',
                ))

    @unittest.skipUnless(os.environ.get('DEP_LINT_LIBS'), 'set DEP_LINT_LIBS to run Maven integration')
    def test_maven_rejects_old_clutter_and_accepts_compatible_range(self):
        spec = '[1.21.1-1.0.197-BETA,1.21.2)'
        old = lint.Check('clutternomore', '3.1.3+1.21.1', 'domum_ornamentum', '1.0.231', spec, 'optional')
        compatible = lint.Check('test', '1', 'domum_ornamentum', '1.0.231', '[1.0.197,1.1)', 'required')
        union = lint.Check('test', '1', 'library', '3.0', '(,1.0],[3.0,)', 'required')
        boundary = lint.Check('test', '1', 'library', '3.0', '[1.0,3.0)', 'required')
        conflicts = lint.compare([old, compatible, union, boundary], os.environ.get('JAVA', 'java'),
                                 Path(os.environ['DEP_LINT_LIBS']), '1.21.1')
        self.assertEqual(conflicts, [old, boundary])

    def test_absent_optional_mod_does_not_fail(self):
        source = mod('example', '1', '''
[[dependencies.example]]
modId="optional_mod"
type="optional"
versionRange="[1,2)"
''')
        mods = lint.inspect_jar(io.BytesIO(source))
        self.assertEqual(lint.dependency_checks('client', mods), ([], []))

    def test_missing_pin_metadata_fails_before_version_comparison(self):
        with self.assertRaisesRegex(ValueError, 'missing=.*123-456'):
            lint.run_lint({}, {'client': ['123-456']}, {}, 'unused', Path('.'))

    @unittest.skipUnless(os.environ.get('DEP_LINT_LIBS'), 'set DEP_LINT_LIBS to run Maven integration')
    def test_all_candidate_versions_outside_range_fail(self):
        owner = mod('example', '1', '''
[[dependencies.example]]
modId="library"
type="optional"
versionRange="[3,4)"
side="CLIENT"
''')
        providers = lint.inspect_jar(io.BytesIO(mod('library', '1')), nested=True)
        providers += lint.inspect_jar(io.BytesIO(mod('library', '2')), nested=True)
        pins = ['123-456', '789-123']
        records = dict(zip(pins, [
            {'sha256': 'a' * 64, 'kind': 'mod', 'mods': lint.inspect_jar(io.BytesIO(owner))},
            {'sha256': 'b' * 64, 'kind': 'mod', 'mods': providers},
        ]))
        stderr = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
            result = lint.run_lint({'minecraft_version': '1.21.1', 'loader_id': 'neoforge-21.1.266'},
                                   {'client': pins, 'server': pins}, records, os.environ.get('JAVA', 'java'),
                                   Path(os.environ['DEP_LINT_LIBS']))
        self.assertEqual(result, 1)
        self.assertIn("[client] example 1 requires library '[3,4)' (optional); candidate versions 1, 2", stderr.getvalue())
        self.assertNotIn('[server]', stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
