# 公開手順

CurseForge project `1733082` への client / server 提出と公開確認の手順です。API の受付、審査、公開、Server Pack 区分は別々に確認します。

## 提出から公開完了まで

1. [開発・ビルド手順](development.md)に従って入力を編集し、PRのCIで生成ZIP・移行差分・秘密情報検査・内容の再現性を確認してmainへマージします。
2. Actionsの **Manual client and server submission** をmainから`submit=false`で起動し、生成物とreceiptを確認します。
3. 確認したmainから`submit=true`で起動します。`manual_release=true`なら審査後も作者の手動公開を待ちます。審査後の自動公開まで進める場合はfalseを選びます。
4. client/serverの審査後、作者画面で親clientの追加serverを開き、**Additional File Info → Server Pack** を選んで保存します。同じ受付済みファイルを編集し、再アップロードしません。
5. **Read-only publication verification** のreceiptで `publication_complete: true` を確認します。両方のApproved、親子関係、Server Pack区分、CDNの全SHAが揃って初めて公開完了です。

main限定の手動workflowです。タグpushだけでは投稿しません。投稿jobは既存`curseforge` Environmentを使います。公開前に Environment の保護ルールと認証設定を確認してください。

同じrunのartifact IDを固定し、両ZIPとsource SHAを再検証します。GET audit通過後に検証済みZIPをGitHub Releaseへ保存し、client受付IDを`parentFileID`としてServer Packを提出します。新しいタグ`v<version>`はそのmain commitに作ります。既存同名assetはSHA/サイズ一致時だけ再利用し、上書きしません。API受付・審査・公開・Server Pack区分は別の状態です。0.0.2 では、Upload API の parentFileID 指定だけでは一般の Additional File として受理されました。公式Upload APIにServer Pack区分の設定方法は記載されていないため、未確認の`isServerPack`等は送りません。作者画面で設定できることを実際に確認しています。

POST前claimと受付後resultをReleaseへ上書きなしで記録します。結果のあるファイルを再送せず、claimだけなら新しい手動起動でも停止します。`mode=server_only`で既存の親を使えます。外部で提出済みの親は`existing_client_file_id`を指定すると、公開状態と公式CDNの全SHAが一致した場合だけ採用します。受付不明は作者画面/receiptを確認してから対応し、ファイル削除や盲目的な再投稿はしません。

公開済み0.0.1のclient9097617/server9104102は`publication-state.json`で保全しています。同版別バイトの提出を拒否します。

## 認証と審査

提出前の GET audit で認証と対象 project を確認します。過去の成功記録だけでは現在の認証を確認できません。同じ版名が複数種別に存在するため、公式の`gameVersionNames`を使用し数値IDは推測しません。childは親の版情報を継承し、独自のgameVersions/gameVersionNamesを送りません。診断には空白等のboolean、固定分類と、既知のAPI用語だけを残したエラー説明を保存します。token値・URL・メール・未知の値は伏せ、tokenの先頭文字・長さ・ハッシュや生の応答本文を出しません。

[作者 Upload token](https://authors.curseforge.com/#/settings/api-tokens)は GitHub の `curseforge` Environment の secret `CURSEFORGE_API_TOKEN` に設定します。実提出には Environment variable `CURSEFORGE_SUBMISSION_ENABLED=true` も必要です。`X-Api-Token`を使い、Core APIのキーとは区別します。

[公式審査規約](https://support.curseforge.com/support/solutions/articles/9000197279-project-and-modpack-moderation-policies)のApp形式・manifest編集制限を踏まえ、標準packwizで新規生成します。App出力を加工して出所を偽装しません。本packの0.0.2はこの方式で公開済みですが、次版や動作の保証とは分けて扱います。

MODの実機動作、全依存グラフ、審査受理は静的検査の範囲外です。自作部分はMIT、第三者のMOD/Shader/設定コメント等の権利は各作者のままです。[LICENSE](../LICENSE)と[配布物のライセンス通知](../pack/overrides/THIRD-PARTY-NOTICES.txt)を参照してください。

## 公開後の検証

`verify-publication.yml`は、実提出workflowの成功後にmainの読み取り権限だけで動きます。Upload tokenもCore API keyも使わず、Releaseの受付journalとZIP digest、公開Web APIのApproved、公開追加ファイルの親ID、Server Pack区分、両CDNの全SHAを検証します。公開Web APIの応答形式が変わった場合も完了と推測しません。

審査待ちは最大10分読み取りで待ちます。その時点でまだ審査中ならreceiptは `publication_complete: false` の待機状態です。workflowが成功しただけでは公開完了と判断しません。審査後に区分を設定して専用workflowを手動起動し、完了receiptを確認します。Approvedでも区分未設定、親ID不一致、SHA不一致、型の判断が曖昧なら検証を失敗させます。`submit=false`だけの通常preflightは自動検証を起動しません。

0.0.2 の受付 ID、区分設定、公開確認の根拠は [提出記録](../CHANGELOG.md#002-submission-evidence)にあります。
