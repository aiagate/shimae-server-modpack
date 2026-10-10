# Shimae Server Modpack

Minecraft 1.21.1 / NeoForge 21.1.243。リポジトリの固定MOD参照と設定から、標準packwizでclient manifest ZIPと軽量Server Packを生成し、GitHub ActionsからCurseForge project **1733082**へ親子提出します。通常の更新に手動App Exportは不要です。Upload APIの提出は自動化していますが、追加ファイルの **Server Pack区分は作者画面で設定**します。公開後の専用検証が、この区分まで確認します。

## 更新するもの

- `pack/release.json`：版、ゲーム/loader、公開種別。今回は0.0.2。
- `pack/client.refs.json`：clientのprojectID/fileID。日常のMOD更新はfile IDを明示してレビューします。自動で最新版へ更新しません。
- `pack/server.refs.json`：serverで使うclientの部分集合。同じprojectのfile IDはclientと一致させます。
- `pack/overrides/`：配布する設定・ライセンス文書。world、接続先、パスワード、履歴を入れません。
- `CHANGELOG.md`：今回の変更、導入方式、動作確認の範囲。

0.0.2への移行ではclient199参照、server189参照、client override320ファイル（設定318＋ライセンス2）、server設定309を保持しています。App由来0.0.1の固定参照・設定SHAと完全照合します。旧Appの出所・設定ポリシー・準備記録は[`CHANGELOG.md`](CHANGELOG.md#001-app-migration-evidence)に統合しています。元のJSON記録は同節の固定Git snapshotから参照できます。通常ビルドはこれらの履歴を参照しません。初回移行の参照・設定SHAは`pack/migration.json`で照合します。

## 公開する操作

1. 上記を編集し、PRのCIで生成ZIP・移行差分・秘密情報検査・内容の再現性を確認してmainへマージします。
2. Actionsの **Manual client and server submission** をmainから`submit=false`で起動し、生成物とreceiptを確認します。
3. 確認したmainから`submit=true`で起動します。`manual_release=true`なら審査後も作者の手動公開を待ちます。審査後の自動公開まで進める場合はfalseを選びます。
4. client/serverの審査後、作者画面で親clientの追加serverを開き、**Additional File Info → Server Pack** を選んで保存します。同じ受付済みファイルを編集し、再アップロードしません。
5. **Read-only publication verification** のreceiptで `publication_complete: true` を確認します。両方のApproved、親子関係、Server Pack区分、CDNの全SHAが揃って初めて公開完了です。

main限定の手動workflowです。タグpushだけでは投稿しません。投稿jobは既存`curseforge` Environmentを使います。required reviewerは未設定なので、上記の手動起動が公開の意思確認です。Secret/保護ルールはこの変更で更新しません。

同じrunのartifact IDを固定し、両ZIPとsource SHAを再検証します。GET audit通過後に検証済みZIPをGitHub Releaseへ保存し、client受付IDを`parentFileID`としてServer Packを提出します。新しいタグ`v<version>`はそのmain commitに作ります。既存同名assetはSHA/サイズ一致時だけ再利用し、上書きしません。API受付・審査・公開・Server Pack区分は別の状態です。Upload APIでparentFileIDを指定するだけでは、今回のserverは一般のAdditional Fileとして受理されました。公式Upload APIにServer Pack区分の設定方法は記載されていないため、未確認の`isServerPack`等は送りません。作者画面で設定できることを実際に確認しています。

POST前claimと受付後resultをReleaseへ上書きなしで記録します。結果のあるファイルを再送せず、claimだけなら新しい手動起動でも停止します。`mode=server_only`で既存の親を使えます。外部で提出済みの親は`existing_client_file_id`を指定すると、公開状態と公式CDNの全SHAが一致した場合だけ採用します。受付不明は作者画面/receiptを確認してから対応し、ファイル削除や盲目的な再投稿はしません。

公開済み0.0.1のclient9097617/server9104102は`publication-state.json`で保全しています。同版別バイトの提出を拒否します。

## 生成方式と配布内容

packwizは`v0.0.0-20260218225342-dfd8b68a4796`、Goは1.27.2で固定し、コンパイラーと本体module checksumを検証します。固定CF参照だけを一時的なpackwiz export入力へ変換します。これはCF export専用で、packwiz-installer向けのMODハッシュを捏造しません。依存の自動追加、MOD取得、アップデート、Minecraft実行はしません。export自体はAPIキー不要・オフラインです。

標準toolが新しくmanifestとmodlistを生成します。App原本のmanifestをJSON置換しません。生成後はentry本文を変えず、順序・時刻・属性を固定した無圧縮ZIPへ再包装します。 packwizのMOD列挙順序は再実行で変わるため、再ビルドのZIPハッシュ一致は保証しません。CIではMOD参照・設定の内容一致を検証し、提出は同じ実行で保存した成果物のハッシュを照合します。受理済み版の再ビルドは別のZIPとして停止し、二重提出しません。client manifest version、表示版、出力名、タグは`pack/release.json`の版に揃えます。既存App originを新しいtool生成ZIPの出所として表示しません。

clientにはMOD/Shaderを199固定IDで参照するmanifestと設定を入れ、JARを同梱しません。serverにも同じclient manifestをバイトそのまま保持します。`SERVER-REFERENCES.json`にserver189参照を記録し、同梱Composeで10 project IDを除外、189を保持します。client用9設定を除いた309設定とライセンス文書、導入手順を付属します。

標準[itzg AUTO_CURSEFORGE](https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/mod-platforms/auto-curseforge/)が`CF_MODPACK_ZIP`からmanifestを読み、必要なMODとNeoForgeを取得します。追加Coreキーを一律必須にせず、java21イメージの標準機能を使います。自動取得不可のMODは標準ツールの指示どおり正確なfile IDをブラウザで取得しdownloadsへ置きます。Upload tokenはMinecraftサーバーへ渡しません。

このServer Packは導入用ZIPで、単独でJavaサーバーが起動するバイナリセットではありません。新規導入はZIPを残して新しい空フォルダへ展開し、同梱Composeを使用します。EULAは本人が確認して明示します。TrueNASは同等のCustom Appとmountを使います。

既存world移行は別作業です。旧起動場所とlevel-nameを確認し、停止したworldの整合性あるコピー等を新しい/dataで使います。旧`CURSEFORGE`は`CF_BASE_DIR`（既定/data/FeedTheBeast）で起動する場合があり、TYPE変更だけではworld移行できません。運用設定・秘密値はローカルで保持します。本番変更・実機起動試験は行っていません。

## 認証と審査の範囲

[mainのGET audit](https://github.com/aiagate/shimae-server-modpack/actions/runs/37880105945)はHTTP200で成功済みです。同じ版名が複数種別に存在するため、公式の`gameVersionNames`を使用し数値IDは推測しません。childは親の版情報を継承し、独自のgameVersions/gameVersionNamesを送りません。診断には空白等のboolean、固定分類と、既知のAPI用語だけを残したエラー説明を保存します。token値・URL・メール・未知の値は伏せ、tokenの先頭文字・長さ・ハッシュや生の応答本文を出しません。

[作者Upload token](https://authors.curseforge.com/#/settings/api-tokens)を[GitHub curseforge Environment](https://github.com/aiagate/shimae-server-modpack/settings/environments/23755335004/edit)の`CURSEFORGE_API_TOKEN`へ本人が設定済みです。`X-Api-Token`を使い、Core APIのキーとは区別します。

[公式審査規約](https://support.curseforge.com/support/solutions/articles/9000197279-project-and-modpack-moderation-policies)のApp形式・manifest編集制限を踏まえ、標準packwizで新規生成します。App出力を加工して出所を偽装しません。本packの0.0.2はこの方式で公開済みですが、次版や動作の保証とは分けて扱います。

MODの実機動作、全依存グラフ、審査受理は静的検査の範囲外です。自作部分はMIT、第三者のMOD/Shader/設定コメント等の権利は各作者のままです。自作の設定変更・リリーススクリプト・文書へのMITライセンスは[`LICENSE`](LICENSE)を参照してください。第三者が生成した既定設定本文・コメント等をMITで再ライセンスするものではありません。参照するMOD/Shaderの利用条件は生成されるmodlist.htmlと各原作者のライセンスに従います。配布用の適用範囲説明は[`pack/overrides/THIRD-PARTY-NOTICES.txt`](pack/overrides/THIRD-PARTY-NOTICES.txt)に保持しています。

## 公開後の検証

`verify-publication.yml`は、実提出workflowの成功後にmainの読み取り権限だけで動きます。Upload tokenもCore API keyも使わず、Releaseの受付journalとZIP digest、公開Web APIのApproved、公開追加ファイルの親ID、Server Pack区分、両CDNの全SHAを検証します。公開Web APIの応答形式が変わった場合も完了と推測しません。

審査待ちは最大10分読み取りで待ちます。その時点でまだ審査中ならreceiptは `publication_complete: false` の待機状態です。workflowが成功しただけでは公開完了と判断しません。審査後に区分を設定して専用workflowを手動起動し、完了receiptを確認します。Approvedでも区分未設定、親ID不一致、SHA不一致、型の判断が曖昧なら検証を失敗させます。`submit=false`だけの通常preflightは自動検証を起動しません。

0.0.2はclient `9104708` / server `9104783`がApprovedで、同じserver受付済みファイルのServer Pack区分を作者画面で設定しました。公開APIの区分・親子関係・CDN全SHAも一致しています。元のZIPと公開済み0.0.1は保持しています。

## 開発と保全

ローカル検証は `python3 -m unittest discover -s tests -v`。固定packwizを用意し、`python3 scripts/native_pack.py --output <新しい出力先> --packwiz <binary>`で両ZIPを生成します。CIは同じビルドを独立に2回実行し、参照と設定の内容一致を確認してレビュー用artifactを保存します。実提出を伴わないCIにUpload tokenは渡しません。

[`CHANGELOG.md`](CHANGELOG.md#002-submission-evidence)に公開済み版の受付ID・SHA・回復経緯を記録しています。完了した0.0.2専用の回復操作は退役しました。現行の`server_only`、公開済み親のバイト照合、immutable claim/result、失敗receiptは保持しています。受付不明のclaimがあれば再送せず、作者画面とreceiptを確認します。

Gitには配布ZIP・MOD JAR・私的な運用資料を入れません。公開済みRelease/ZIP、App原本、監査receipt、ローカル運用資料はcleanupの対象外です。
