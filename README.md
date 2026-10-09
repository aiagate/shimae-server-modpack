# Shimae Server Modpack

Minecraft 1.21.1 / NeoForge 21.1.243。リポジトリの固定MOD参照と設定から、標準packwizでclient manifest ZIPと軽量Server Packを生成し、GitHub ActionsからCurseForge project **1733082**へ親子提出します。通常の更新に手動App Exportは不要です。

## 更新するもの

- `pack/release.json`：版、ゲーム/loader、公開種別。今回は0.0.2。
- `pack/client.refs.json`：clientのprojectID/fileID。日常のMOD更新はfile IDを明示してレビューします。自動で最新版へ更新しません。
- `pack/server.refs.json`：serverで使うclientの部分集合。同じprojectのfile IDはclientと一致させます。
- `pack/overrides/`：配布する設定・ライセンス文書。world、接続先、パスワード、履歴を入れません。
- `CHANGELOG.md`：今回の変更、導入方式、動作確認の範囲。

0.0.2への移行ではclient199参照、server189参照、client override320ファイル（設定318＋ライセンス2）、server設定309を保持しています。App由来0.0.1の固定参照・設定SHAと完全照合します。旧`exports/**`とルートの`release.json`は移行証跡と過去の検査用で、通常ビルドの入力ではありません。

## 公開する操作

1. 上記を編集し、PRのCIで生成ZIP・移行差分・秘密情報検査・内容の再現性を確認してmainへマージします。
2. Actionsの **Manual client and server submission** をmainから`submit=false`で起動し、生成物とreceiptを確認します。
3. 確認したmainから`submit=true`で起動します。`manual_release=true`なら審査後も作者の手動公開を待ちます。審査後の自動公開まで進める場合はfalseを選びます。

main限定の手動workflowです。タグpushだけでは投稿しません。投稿jobは既存`curseforge` Environmentを使います。required reviewerは未設定なので、上記の手動起動が公開の意思確認です。Secret/保護ルールはこの変更で更新しません。

同じrunのartifact IDを固定し、両ZIPとsource SHAを再検証します。GET audit通過後に検証済みZIPをGitHub Releaseへ保存し、client受付IDを`parentFileID`としてServer Packを提出します。新しいタグ`v<version>`はそのmain commitに作ります。既存同名assetはSHA/サイズ一致時だけ再利用し、上書きしません。API受付・審査・公開は別の状態です。

POST前claimと受付後resultをReleaseへ上書きなしで記録します。結果のあるファイルを再送せず、claimだけなら新しい手動起動でも停止します。`mode=server_only`で既存の親を使えます。外部で提出済みの親は`existing_client_file_id`を指定すると、公開状態と公式CDNの全SHAが一致した場合だけ採用します。受付不明は作者画面/receiptを確認してから対応し、ファイル削除や盲目的な再投稿はしません。

公開済み0.0.1のclient9097617/server9104102は`publication-state.json`で保全しています。同版別バイトの提出を拒否します。

## 生成方式と配布内容

packwizは`v0.0.0-20260218225342-dfd8b68a4796`、Goは1.27.2で固定し、コンパイラーと本体module checksumを検証します。固定CF参照だけを一時的なpackwiz export入力へ変換します。これはCF export専用で、packwiz-installer向けのMODハッシュを捏造しません。依存の自動追加、MOD取得、アップデート、Minecraft実行はしません。export自体はAPIキー不要・オフラインです。

標準toolが新しくmanifestとmodlistを生成します。App原本のmanifestをJSON置換しません。生成後はentry本文を変えず、順序・時刻・属性を固定した無圧縮ZIPへ再包装します。 packwizのMOD列挙順序は再実行で変わるため、再ビルドのZIPハッシュ一致は保証しません。CIではMOD参照・設定の内容一致を検証し、提出は同じ実行で保存した成果物のハッシュを照合します。受理済み版の再ビルドは別のZIPとして停止し、二重提出しません。client manifest version、表示版、出力名、タグは`pack/release.json`の版に揃えます。既存App originを新しいtool生成ZIPの出所として表示しません。

clientにはMOD/Shaderを199固定IDで参照するmanifestと設定を入れ、JARを同梱しません。serverにも同じclient manifestをバイトそのまま保持します。`SERVER-REFERENCES.json`にserver189参照を記録し、同梱Composeで10 project IDを除外、189を保持します。client用9設定を除いた309設定とライセンス文書、導入手順を付属します。

標準[itzg AUTO_CURSEFORGE](https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/mod-platforms/auto-curseforge/)が`CF_MODPACK_ZIP`からmanifestを読み、必要なMODとNeoForgeを取得します。追加Coreキーを一律必須にせず、java21イメージの標準機能を使います。自動取得不可のMODは標準ツールの指示どおり正確なfile IDをブラウザで取得しdownloadsへ置きます。Upload tokenはMinecraftサーバーへ渡しません。

このServer Packは導入用ZIPで、単独でJavaサーバーが起動するバイナリセットではありません。新規導入はZIPを残して新しい空フォルダへ展開し、同梱Composeを使用します。EULAは本人が確認して明示します。TrueNASは同等のCustom Appとmountを使います。

既存world移行は別作業です。旧起動場所とlevel-nameを確認し、停止したworldの整合性あるコピー等を新しい/dataで使います。旧`CURSEFORGE`は`CF_BASE_DIR`（既定/data/FeedTheBeast）で起動する場合があり、TYPE変更だけではworld移行できません。運用設定・秘密値はローカルで保持します。添付済みTrueNAS composeの正式取得は失敗しているため、本番構成の確定差分とはしません。本番変更・実機起動試験は行っていません。

## 認証と審査の範囲

[mainのGET audit](https://github.com/aiagate/shimae-server-modpack/actions/runs/37880105945)はHTTP200で成功済みです。同じ版名が複数種別に存在するため、公式の`gameVersionNames`を使用し数値IDは推測しません。childは親の版情報を継承し、独自のgameVersions/gameVersionNamesを送りません。診断には空白等のboolean、固定分類と、既知のAPI用語だけを残したエラー説明を保存します。token値・URL・メール・未知の値は伏せ、tokenの先頭文字・長さ・ハッシュや生の応答本文を出しません。

[作者Upload token](https://authors.curseforge.com/#/settings/api-tokens)を[GitHub curseforge Environment](https://github.com/aiagate/shimae-server-modpack/settings/environments/23755335004/edit)の`CURSEFORGE_API_TOKEN`へ本人が設定済みです。`X-Api-Token`を使い、Core APIのキーとは区別します。

[公式審査規約](https://support.curseforge.com/support/solutions/articles/9000197279-project-and-modpack-moderation-policies)にはAppでの作成・App生成manifestの編集禁止が書かれています。一方、[TerraFirmaGregのPakku workflow](https://github.com/TerraFirmaGreg-Team/Modpack-Modern/blob/305ea8e4a54025b0b46fdc4cfc27ff96611dc3c3/.github/workflows/build.yml)と[公開ファイル](https://www.curseforge.com/minecraft/modpacks/terrafirmagreg-modern/files/8037324)、[Trashlandsのpackwiz workflow](https://github.com/Flatts3000/trashlands/blob/6e8748be14363ff03ecfdb493ee061ea9f605094/.github/workflows/release.yml)には標準toolでの生成・API提出の実績があります。他projectの実績は、本projectや軽量Server Packの審査保証ではありません。今回の方式はrepository-owned source/packwiz outputと明示し、App生成という虚偽の出所にはしません。手動App Exportが唯一の方法とは扱いません。

MODの実機動作、全依存グラフ、審査受理は静的検査の範囲外です。自作部分はMIT、第三者のMOD/Shader/設定コメント等の権利は各作者のままです。LICENSEとLICENSE-SCOPE.txtを参照してください。

## 0.0.2 server提出の回復

最初のActions run `37883897099`はclient `9104708`を受け付け、serverはHTTP400/error1013で停止しました。作者画面で親のApproved/公開と追加server未登録を確認しています。原因は未確定です。任意のchild版名指定を省き、公開APIライブラリと同様に親の版情報を継承します。

専用 **Recover saved 0.0.2 server submission** は旧Releaseの正確な両ZIP、元runのreceipt、受付済み親の公開状態/CDN全SHAを照合します。clientを再投稿せず、元server claimも残し、別の一度限りrecovery claimをPOST前に保存します。受付IDは元server resultへ記録します。受付不明の回復claimがある場合は再実行しても停止し、勝手に削除しません。既定はsubmit=falseです。この回復は0.0.2の失敗に限定し、通常の版更新用ではありません。
