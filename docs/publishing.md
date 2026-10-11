# 公開手順

CurseForge project `1733082` への client / server 提出と公開確認の手順です。API の受付、審査、公開、Server Pack 区分は別々に確認します。

## 提出から公開完了まで

1. [開発・ビルド手順](development.md)に従って入力を編集し、PRのCIで生成ZIP・移行差分・秘密情報検査・内容の再現性を確認してmainへマージします。
2. Actionsの **Release / Submit** をmainから`submit=true`で起動します。preflight が生成した ZIP と receipt を、その run の summary のリンクから確認します。
3. 内容を確認したら、同じ run の `curseforge` Environment の deployment を承認します。提出 job はその run の成果物をダウンロードし、再ビルドせずに提出します。`manual_release=true`なら審査後も作者の手動公開を待ちます。審査後の自動公開まで進める場合はfalseを選びます。
4. server提出時に `parentFileID` と `isServerPack: true` を送り、区分の自動設定を試みます。審査後の公開検証で区分を確認します。未設定・判断不能なら receipt の `required_action` に記録された同じ受付済み server を作者画面で確認し、必要なら **Additional File Info → Server Pack** を保存します。再アップロードしません。
5. **Release / Verify publication** のreceiptで `publication_complete: true` を確認します。両方のApproved、親子関係、Server Pack区分、CDNの全SHAが揃って初めて公開完了です。

main限定の手動workflowです。タグpushだけでは投稿しません。投稿jobは既存`curseforge` Environmentを使います。`curseforge` Environment に required reviewers を設定してください。提出を要求した run は、レビュアー設定がない場合や設定を取得できない場合、preflight で停止します。承認は成果物の確認後に行います。`submit=false` は提出しない独立した検証用で、その成果物を後続の別 run へ引き継ぐ用途には使いません。

同じrunのartifact IDを固定し、両ZIPとsource SHAを再検証します。GET audit通過後に検証済みZIPをGitHub Releaseへ保存し、client受付IDを`parentFileID`としてServer Packを提出します。新しいタグ`v<version>`はそのmain commitに作ります。既存同名assetはSHA/サイズ一致時だけ再利用し、上書きしません。API受付・審査・公開・Server Pack区分は別の状態です。`isServerPack` は公式 Upload API に未文書化のため、自動分類の成功を受付 ID から推測しません。[Xikaro 1.1.1 の配布コード](https://github.com/Xikaro/upload-curseforge-modpack-action/blob/1.1.1/dist/index.js#L53-L62)と[HaXrDEV の実装](https://github.com/HaXrDEV/upload-curseforge-modpack-action/blob/master/index.js)を参考にした試行です。現行サービスでの効果は未検証です。

POST前claimと受付後resultをReleaseへ上書きなしで記録します。結果のあるファイルを再送せず、claimだけなら新しい手動起動でも停止します。`mode=server_only`で既存の親を使えます。外部で提出済みの親は`existing_client_file_id`を指定すると、公開状態と公式CDNの全SHAが一致した場合だけ採用します。受付不明は作者画面/receiptを確認してから対応し、ファイル削除や盲目的な再投稿はしません。

公開済み0.0.1のclient9097617/server9104102は`publication-state.json`で保全しています。同版別バイトの提出を拒否します。

## 認証と審査

提出前の GET audit で認証と対象 project を確認します。過去の成功記録だけでは現在の認証を確認できません。同じ版名が複数種別に存在するため、公式の`gameVersionNames`を使用し数値IDは推測しません。childは親の版情報を継承し、独自のgameVersions/gameVersionNamesを送りません。提出前の GET audit の診断には空白等のboolean、固定分類と、既知のAPI用語だけを残したエラー説明を保存します。token値・URL・メール・未知の値は伏せ、tokenの先頭文字・長さ・ハッシュや生の応答本文を出しません。

[作者 Upload token](https://authors.curseforge.com/#/settings/api-tokens)は GitHub の `curseforge` Environment の secret `CURSEFORGE_API_TOKEN` に設定します。実提出には Environment variable `CURSEFORGE_SUBMISSION_ENABLED=true` も必要です。`X-Api-Token`を使い、Core APIのキーとは区別します。

[公式審査規約](https://support.curseforge.com/support/solutions/articles/9000197279-project-and-modpack-moderation-policies)のApp形式・manifest編集制限を踏まえ、標準packwizで新規生成します。

MODの実機動作、全依存グラフ、審査受理は静的検査の範囲外です。自作部分はMIT、第三者のMOD/Shader/設定コメント等の権利は各作者のままです。[LICENSE](../LICENSE)と[配布物のライセンス通知](../pack/overrides/THIRD-PARTY-NOTICES.txt)を参照してください。

## 公開後の検証

`verify-publication.yml` は、Submit 内の提出 job が成功した場合だけ reusable workflow として呼び出します。別の workflow_run による自動起動は行いません。main からの手動起動も可能です。検証 job は main の読み取り権限だけで動きます。Upload tokenもCore API keyも使わず、Releaseの受付journalとZIP digest、公開Web APIのApproved、公開追加ファイルの親ID、Server Pack区分、両CDNの全SHAを検証します。公開Web APIの応答形式が変わった場合も完了と推測しません。

審査待ちは最大10分読み取りで待ちます。その時点でまだ審査中ならreceiptは `publication_complete: false` の待機状態です。workflowが成功しただけでは公開完了と判断しません。審査後に区分を再確認し、必要な作者画面の保存後は専用workflowだけを手動起動して完了receiptを確認します。Approvedでも区分未設定、親ID不一致、SHA不一致、型の判断が曖昧なら検証を失敗させます。`submit=false`だけの通常preflightは自動検証を起動しません。

0.0.2 の受付 ID、区分設定、公開確認の根拠は [提出記録](release-history.md#002-submission-evidence)にあります。

## 次の実リリースでの自動分類確認

この変更の単体テスト・CIは metadata の送出、無条件再送の禁止、公開検証の停止条件までを検証します。本番での自動分類成功は検証しません。公開済み0.0.4を使った再提出・編集は行いません。

次の通常リリースが別途承認されたら、同 run の server metadata に `isServerPack: true` が含まれることを preflight plan で確認します。提出後、作者画面で区分を変更する前に Verify publication の receipt を確認します。両 Approved・正しい親ID・Server Pack区分・全CDN SHAが一致し `publication_complete: true` なら、そのリリースで自動分類まで確認できたと扱います。

区分未設定・曖昧なら status は `server_pack_setting_required_or_ambiguous`、`required_action` は正確な project/client/server ID と作者画面での確認操作、`retry_submission: false` を残します。審査待ちなら読み取り検証だけを継続します。APIが未文書化フィールドを拒否した場合も自動でフィールドを外して再POSTしません。診断 receipt・claim/result・作者画面で受付有無を調べ、確認結果と次の対応をレビューします。受付不明の claim は別 run でも再提出を止めます。既存token・承認付き Environment の範囲を保ち、ブラウザ認証を利用しません。
