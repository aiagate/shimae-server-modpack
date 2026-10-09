"""One reviewed recovery of the HTTP400 child request; never resend client."""
import argparse,json,os
from pathlib import Path
import native_pack as native
import publish_pair as pair
import release
import serverpack

PROJECT=1733082
VERSION='0.0.2'
CLIENT_ID=9104708
SOURCE_RUN=37883897099
CLIENT_SHA='f9f14a87d8ed5589c5f619af35786147b0ecbfa56247346f5b2122f2f27b82c9'
SERVER_SHA='49c213f137d56afabc245d6839706b0f181c034b90753e23e3b5616c5adf660a'
IDENTITY=pair.fingerprint(PROJECT,VERSION,CLIENT_SHA,SERVER_SHA)
EVIDENCE={
    'source_run_id':SOURCE_RUN,'http_status':400,'error_code':1013,
    'author_ui_checked_date':'2026-10-09','parent_file_id':CLIENT_ID,
    'parent_status_observed':'Approved/public','additional_server_files_observed':0,
    'metadata_change':'omit_optional_gameVersionNames; inherit parent versions',
    'cause_confirmed':False,
}


def verify_saved(directory):
    inputs=native.load_inputs()
    release.need(inputs[0]['version']==VERSION and inputs[0]['project_id']==PROJECT,'source version/project changed')
    client=directory/f'shimae-server-modpack-{VERSION}.zip'
    server=directory/f'shimae-server-modpack-{VERSION}-serverpack.zip'
    c=release.parse_json((directory/'client.json').read_bytes())
    s=release.parse_json((directory/'server.json').read_bytes())
    release.need(native.verify_client(client,c,inputs)==CLIENT_SHA and serverpack.sha(server)==SERVER_SHA,
        'recovery must use the original saved ZIP bytes')
    serverpack.verify_prepared(server,s,client,native.policy(inputs[2]),VERSION,inputs[1])
    failure=release.parse_json((directory/'submission-result.json').read_bytes())
    release.need(all(failure.get(k)==v for k,v in IDENTITY.items()) and
        failure.get('client_file_id')==CLIENT_ID and failure.get('server_file_id') is None and
        failure.get('pending_kind')=='server' and failure.get('status')=='submission_unconfirmed' and
        failure.get('error',{}).get('http_status')==400 and
        failure['error'].get('response_summary',{}).get('error_code')==1013,
        'original failed server receipt differs; no recovery')
    return client,server,native.runtime_config(inputs[0],CLIENT_SHA)


class RecoveryJournal(pair.GitHubJournal):
    def claim(self,kind):
        release.need(kind=='server','client must never be sent by this recovery')
        original=self.read('server','claim')
        release.need(original is not None,'original server claim required')
        release.need(all(original.get(k)==v for k,v in IDENTITY.items()),'original claim identity differs')
        release.need(self.read('server','recovery-1-claim') is None,'recovery already attempted; inspect result before any retry')
        record=dict(schema_version=1,**IDENTITY,kind='server',status='recovery_claimed',evidence=EVIDENCE)
        # Exclusive asset creation: a previous attempt, even one without a result,
        # blocks this recovery. Preserve both the original claim and its receipt.
        self.write('server','recovery-1-claim',record)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,required=True)
    parser.add_argument('--receipt',type=Path,required=True)
    parser.add_argument('--submit',action='store_true')
    args=parser.parse_args()
    try:
        release.need(not args.receipt.exists(),'use a new receipt path')
        client,server,config=verify_saved(args.directory)
        plan=dict(schema_version=1,**IDENTITY,status='dry_run_no_post',evidence=EVIDENCE,
            server_metadata=pair.server_metadata(config,VERSION,Path('CHANGELOG.md').read_text(),CLIENT_ID,False))
        if not args.submit:
            args.receipt.write_text(json.dumps(plan,indent=2)+'\n');print(json.dumps(plan,indent=2));return 0
        release.need(os.environ.get('GITHUB_REF')=='refs/heads/main','recovery is main-only')
        release.need(os.environ.get('CURSEFORGE_SUBMISSION_ENABLED')=='true','submission disabled')
        token=os.environ.get('CURSEFORGE_API_TOKEN','');release.token_check(token)
        import diagnose_api
        audit=diagnose_api.audit(token)
        release.need(audit['status']=='read_complete' and audit.get('missing_names')==[],'read-only authentication audit failed')
        journal=RecoveryJournal('v'+VERSION,IDENTITY)
        parent=journal.read('client','result')
        release.need(parent is not None and pair.check_record(parent,IDENTITY,'client')==CLIENT_ID,
            'saved client acceptance ID differs')
        pair.verify_existing_client(CLIENT_ID,PROJECT,client)
        result=pair.publish(client,server,config,VERSION,Path('CHANGELOG.md').read_text(),IDENTITY,None,journal,
            mode='server_only',manual=False,token=token,receipt=args.receipt)
        print(json.dumps(result,indent=2));return 0
    except release.SubmissionError as error:
        if args.receipt.exists():
            result=release.parse_json(args.receipt.read_bytes());result['error']=error.diagnostics
            args.receipt.write_text(json.dumps(result,indent=2)+'\n')
        print('STOP: server recovery not confirmed; preserve receipt and check author dashboard.')
        return 1
    except (release.Invalid,OSError,ValueError,KeyError):
        print('STOP: saved source/journal recovery checks failed; no successful submission confirmed.')
        return 1

if __name__=='__main__':raise SystemExit(main())
