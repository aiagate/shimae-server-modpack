import copy,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import recover_server_002 as recovery
import publish_pair as pair
import release

class RecoveryTests(unittest.TestCase):
    def test_child_metadata_inherits_versions(self):
        meta=pair.server_metadata({'release_type':'release'},'0.0.2','test',9104708)
        self.assertEqual(meta['parentFileID'],9104708)
        self.assertNotIn('gameVersions',meta);self.assertNotIn('gameVersionNames',meta)
    def test_client_recovery_claim_forbidden(self):
        journal=recovery.RecoveryJournal('v0.0.2',recovery.IDENTITY)
        with self.assertRaises(release.Invalid):journal.claim('client')
    def test_original_claim_retained_and_one_exclusive_recovery_claim(self):
        journal=recovery.RecoveryJournal('v0.0.2',recovery.IDENTITY)
        original=dict(recovery.IDENTITY,kind='server')
        with patch.object(journal,'read',side_effect=[original,None]),patch.object(journal,'write') as write:
            journal.claim('server')
            kind,phase,record=write.call_args.args
            self.assertEqual((kind,phase),('server','recovery-1-claim'))
            self.assertEqual(record['evidence']['additional_server_files_observed'],0)
    def test_uncertain_recovery_claim_cannot_post_again(self):
        journal=recovery.RecoveryJournal('v0.0.2',recovery.IDENTITY)
        with patch.object(journal,'read',side_effect=[dict(recovery.IDENTITY),{'status':'claimed'}]),patch.object(journal,'write') as write:
            with self.assertRaises(release.Invalid):journal.claim('server')
            write.assert_not_called()
    def test_original_different_bytes_claim_cannot_recover(self):
        journal=recovery.RecoveryJournal('v0.0.2',recovery.IDENTITY)
        original=dict(recovery.IDENTITY,server_sha256='0'*64)
        with patch.object(journal,'read',return_value=original),patch.object(journal,'write') as write:
            with self.assertRaises(release.Invalid):journal.claim('server')
            write.assert_not_called()

if __name__=='__main__':unittest.main()
