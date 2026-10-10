"""Check the real recipe pack reaches both distribution staging paths."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import native_pack
import serverpack

ROOT = Path(__file__).resolve().parents[1] / 'pack'
PREFIX = 'overrides/config/openloader/packs/shimae_coasters/'


class CoastersDistributionTests(unittest.TestCase):
    def test_recipe_pack_is_valid_for_target_version_and_distributed_to_both_sides(self):
        meta, refs, overrides, _ = native_pack.load_inputs(ROOT)
        files = {n: b for n, b in overrides.items() if n.startswith(PREFIX)}
        self.assertEqual(json.loads(files[PREFIX + 'pack.mcmeta'])['pack']['pack_format'], 48)
        recipes = {n: json.loads(b) for n, b in files.items() if n.endswith('.json')}
        self.assertEqual(len(recipes), 3)
        outputs = set()
        for name, recipe in recipes.items():
            self.assertIn('/data/shimae/recipe/coasters/', name)
            self.assertEqual(recipe['type'], 'minecraft:crafting_shapeless')
            self.assertTrue(1 <= len(recipe['ingredients']) <= 4)
            self.assertTrue(all(set(i) == {'item'} and i['item'].startswith(
                ('minecraft:', 'create:')) for i in recipe['ingredients']))
            self.assertEqual(set(recipe['result']), {'id', 'count'})
            self.assertEqual(recipe['result']['count'], 1)
            outputs.add(recipe['result']['id'])
        self.assertEqual(outputs, {'createcoasters:boost_block',
                                  'createcoasters:speed_block', 'createcoasters:lock_block'})
        for pid in (354339, 1023259, 1298151):
            self.assertEqual(refs['client'][pid], refs['server'][pid])
        with tempfile.TemporaryDirectory() as tmp:
            stage = Path(tmp) / 'stage'
            stage.mkdir()
            native_pack.stage(stage, meta, refs, overrides)
            for name, blob in files.items():
                self.assertEqual((stage / name.removeprefix('overrides/')).read_bytes(), blob)
            client = Path(tmp) / 'client.zip'
            with zipfile.ZipFile(client, 'w') as archive:
                archive.writestr('manifest.json', json.dumps({'version': meta['version']}))
                archive.writestr('modlist.html', '<ul></ul>')
                for name, blob in overrides.items():
                    archive.writestr(name, blob)
            server = serverpack.blobs(client, native_pack.policy(overrides), refs, meta['version'])
            for name, blob in files.items():
                self.assertEqual(server[name], blob)
