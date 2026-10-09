# Shimae Server Modpack

Minecraft `1.21.1` / NeoForge `21.1.243`のModPackを、CurseForge project **1733082**で公開するためのリポジトリです。正式投稿の入力は、本人がCurseForge Appから出力した**クライアントExport ZIP 1つ**です。Appが出力したmanifestは編集しません。サーバープロフィールのExportは公開の前提にしません。

`Shimae Server Modpack-0.0.1.zip`を受領し、199参照と全File IDの一致、MC/loader、CRCと構造を確認しました。原本は保全し、不要状態11件の除外とライセンス文書2件の付属だけを行った提出候補をローカル検査済みです。manifest・modlist・残した設定本文は原本とバイト一致します。GitHub Release asset ID `621353663`を登録済みです。CurseForge提出・審査・公開は別に確認します。Appでの出力操作を独立に観察したという証明は付けません。

## 本人に必要な入力作成

1. CurseForge Appで配布するクライアントプロフィールを開きます。TFC除去済み候補を使う場合も、AppへImportしてプロフィールを確認します。
2. Minecraft `1.21.1` / NeoForge `21.1.243`、TFC・Offset Smoker・Bonsai除外、PatchouliとApotheosis系列の保持を確認します。参照基準は199件です。MOD取得・起動・必要なサーバーへの参加を確認します。
3. Export前に不要なベンチマーク、機器fingerprint、Chunky作業状態、Bonsai client/common設定、個人履歴・バックアップ等を除きます。有効なChunky設定は保持します。必要なライセンス文書はプロフィール側へ配置します。
4. AppのShare Profile → Export as .zipで、mods参照と必要な設定等を選びます。不要状態がなければそのZIPを提出します。版、プロフィール名、Export日時も記録します。今回の0.0.1は受領済みで、追加のExportは現在のローカル検査の前提ではありません。

Export後のmanifestをcheckerのために編集しません。構成や有効な設定の変更が必要な場合は、プロフィール側を直して再Exportします。不要状態の除外だけの場合は、原本を保持し、manifestと残した設定のバイト一致を確認した整理コピーを別に作ります。server用Exportを別途作る必要はありません。

## 受領後の検査・登録

作業側がclient ZIPの名前・版・サイズ・SHA256・manifest名・出所記録を`exports/exports.lock.json`のclientへ登録します。`origin.confirmed=true`は人による確認記録であり、機械がApp出所を証明した意味ではありません。`exports/client.refs.json`と`policy.json`の参照・設定ハッシュを比較し、再Exportによる差異があれば理由をレビューします。提出候補のmanifestと残した設定本文は書き換えません。原本と整理コピーのSHAを別に記録します。

`release.json`はproject ID `1733082`とゲーム版を設定済みです。正式client版・表示名・SHAとCHANGELOGを確定します。公開前のローカル検査ではclient asset IDをnullのまま使えます。

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
python3 scripts/verify_app_exports.py --client /path/client-app-export.zip
python3 scripts/release.py --zip /path/client-app-export.zip
```

`scripts/prepare_export.py`と`exports/preparation.json`で今回の整理を再現できます。原本SHAを固定し、削除はレビュー済み不要状態に限定して、別のZIPを作ります。出所記録はApp Export由来の整理コピーであり、未改変App Export ZIPそのものという表示にはしません。

公開用に検査した提出候補を本リポジトリの公開Release assetへ保存した後、実asset IDをclient lockと`release.json`に同一値で固定します。ZIPはGitへ追跡せず、最新assetを名前や可変URLで推測しません。

## Actionsからクライアント・Server Packを提出する

`validate.yml`はpush/PRでテスト、Python構文、GitのZIP混入、固定assetのApp clientを検査し、軽量サーバー導入ZIPとオフライン提出計画まで作ります。PRで提出・Release作成・artifact保存はしません。

`submit.yml`はmainからの手動起動です。タグpushでは起動しません。`submit=false`では検証と導入ZIP生成だけを行い、同じrunのclient/server ZIPとreceiptを14日間保存します。版を確定し、人が確認してから`submit=true`を指定できます。Environment `curseforge`を使いますが、既存Environmentにrequired reviewerは未設定です。保護ルールの変更は今回行いません。`manual_release=true`が既定で、API受付後も審査後の作者による公開操作を待ちます。完全自動公開を選ぶ場合だけfalseにします。

投稿jobは同じcommit・同じrunのartifact IDを固定し、ZIPのSHAと全内容を再確認します。最初に読み取り専用Upload API auditを行い、通らなければGitHub Release作成もファイルPOSTも行いません。通過した場合は同版Releaseへ検証済み2 ZIPを保存し、clientを提出、返ったfile IDを`parentFileID`としてAdditional Server Packを提出します。子に数値`gameVersions`は送りません。同名GitHub assetはSHAとサイズが一致する場合だけ再利用し、上書きしません。新しい版のReleaseがない場合、実投稿jobだけがそのcommitを指すタグ・Releaseを作成します。

再送防止はGitHub Releaseの永続記録で行います。ファイルPOST前に`curseforge-*-claim.json`、受け付けたIDを得た後に`*-result.json`を追加します（実名には全SHAを含みます）。結果があるファイルは再投稿しません。client成功後のserver失敗ではclient IDを再利用します。claimだけが残る場合は新しい手動起動でも停止します。artifactの有効期限切れやworkflow再実行を理由に再POSTしません。API受付と審査・公開完了は別の状態です。

`mode=server_only`は記録済みclientがある場合の子だけの提出です。記録がなく、作者画面で公開済みclientを特定済みなら`existing_client_file_id`を指定できます。公開メタデータと公式CDNのSHAが検証済みApp clientと一致した場合だけ採用します。未承認・非公開・取得不能・バイト不一致なら停止します。親を新しく投稿して補いません。

通信timeoutなどで受付が不明なら作者画面とsanitized receiptを照合します。receiptに受付IDが残り、Releaseへの結果保存だけが失敗した場合も自動再送しません。確認したfile ID・親ID・同版両SHAを`publication-state.json`へレビュー付きで登録すれば、その受付済みファイルを再利用できます。登録するserverの親IDを確認します。受付なしを確認するまではclaimを削除しません。結果が判明しないまま新しい版へ逃がして再投稿もしません。

既存0.0.1はclient `9097617`、server `9104102`が公開済みです。`publication-state.json`が同版別バイトの投稿を止めます。軽量化した0.0.1をdry-runで確認しても、公開済み同版のServer Packを置き換えたり追加投稿したりしません。

## 認証の切り分けと0.0.2の準備

[読取専用audit 37875776072](https://github.com/aiagate/shimae-server-modpack/actions/runs/37875776072)はHTTP 400、`error_code=3`で失敗しました。ZIPや投稿metadataのないGET `/api/game/versions`でも拒否されています。公式文書にこのコードの意味の一覧はなく、失効や種類違いとは断定しません。追加の対照確認として、秘密値なしのGETはHTTP401、明示的な合成無効トークンのGETはHTTP400/code3となり、後者の応答にはトークン解析・形式エラーを示す文言がありました（本文は保存・表示していません）。これが同じコードを再現する公式API側の観測根拠です。コード3を全場面で特定原因に対応させる公式一覧はなく、実Secretの種類違い・失効まで断定しません。今後のauditではこの文言を`malformed_authentication`という固定分類だけで記録します。既存tokenでAPI投稿できる状態は確認できていません。元のauditでは空・前後空白・制御文字の基本検査を通過し、実際のGET応答を受けています。今回、空白・制御文字・非ASCIIの有無をbooleanだけで記録する診断も追加しました。値・先頭文字・文字数・ハッシュは記録しません。公式にUpload tokenとCore keyを区別する文字列形式の規約は見つからず、文字列の形式やSecretの存在だけでは種類を確定できません。`token_kind_verified_from_format=false`は診断の限界を明示する値です。

本人だけが[作者画面のAPI Tokens](https://authors.curseforge.com/#/settings/api-tokens)でUpload API用tokenを作成・確認し、[GitHub Environment `curseforge`の設定画面](https://github.com/aiagate/shimae-server-modpack/settings/environments/23755335004/edit)のEnvironment secretsから`CURSEFORGE_API_TOKEN`の更新画面を開き、設定します。作者用Upload APIは`X-Api-Token`ヘッダーに生成されたトークンをそのまま渡します。Core APIの`x-api-key`とは別です。GETは公式の`https://minecraft.curseforge.com/api/game/versions`、POSTは同ホストの`/api/projects/{projectId}/upload-file`、multipartの`metadata`/`file`です。実装はこれらの指定と一致しています。チャット、コマンド引数、Git、artifactへ値を出しません。設定後は`diagnose.yml`のGETで確認します。Secret更新・tokenの取得やコピー・アカウント変更をこのPRでは行いません。既存project ID `1733082`を使うため、新しいCurseForge projectの作成は不要です。

0.0.2の正式App clientが届いたら、その原本とmanifestを保全し、版・MOD参照・設定差分をレビューしてclient lock、`release.json`、CHANGELOGを更新します。別のserver App exportは不要です。このPRで0.0.1のmanifestを0.0.2へ書き換えたり、未受領の正式clientを作ったりはしません。変更をmainへ反映する前にPRのCIを確認します。マージ・タグ・実投稿はこの作業の実行範囲外です。

## 検査の範囲と生成案

ZIPのCRC、SHA256、manifest・版・loader・参照ID、危険なパス、重複、symlink、暗号化、サイズ、実行属性、設定の秘密値・私的接続先・不要状態、JSON/TOMLを検査します。参照件数だけで合格にせず、199参照の完全lockと照合します。MODの全依存グラフ、mixins、掲載承認状態、実機動作や配布権利を完全自動証明したとは扱いません。

`exports/server.refs.json`とserver側のpolicyは構成比較用の既存メタデータです。これはserver ZIPの受領を要求するものではありません。既存server側override policyには古い設定SHAがあるため、今回の導入ZIPは検証済みclientの現行config本文を使います。client用9設定を除外し、追加されたApotheosis系列3設定も保持します。

[公式審査規約](https://support.curseforge.com/support/solutions/articles/9000197279-project-and-modpack-moderation-policies)はAppでのModPack作成とApp生成manifestの編集禁止を明記しています。独自の互換ZIP生成はApp起源の証拠になりません。独自生成のローカル修正は別に保持し、今回の正式投稿フローへ混ぜません。

## 軽量サーバー導入ZIPの形式

`scripts/serverpack.py`はApp clientのmanifestとmodlistをバイトそのまま保持し、現行configからclient用9件を除いた309件、ライセンス文書2件、server参照189件の記録、Compose例、導入手順を格納します。ルートは`manifest.json`、`modlist.html`、`SERVER-REFERENCES.json`、`compose.yaml`、`README-SERVER.md`です。`overrides/config/`に309設定、`overrides/`直下にライセンス文書2件を置きます。未変更manifestは**client用199件**です。`SERVER-REFERENCES.json`はserver用189件の記録で、App manifestの代替ではありません。MOD JAR・loader・Java・world・EULA同意・認証情報を同梱しません。0.0.1材料による静的検査では3,034,375 bytesです。主成分はconfig本文2,903,312 bytesです。エントリ順、時刻、属性を固定し、圧縮ライブラリによる差を避けて無圧縮ZIPにしています。公開済み683 MB版は変更しません。2つのZIPは役割が違います。

標準の[itzg AUTO_CURSEFORGE](https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/mod-platforms/auto-curseforge/)はローカルZIPを`CF_MODPACK_ZIP`で読めます。Composeは元ZIPを残して展開した新規フォルダから起動する例です。manifestの199件を編集せず、`CF_EXCLUDE_MODS`で10件を除外、`CF_FORCE_INCLUDE_MODS`で意図した189件を指定します。設定はZIPのoverridesから導入されます。java21イメージは現在Core API keyを内蔵しているため、追加キーの作成は一律必須にしません。自前キーを使う場合はDocker secret等で渡します。自動取得が禁止されたMODは標準ツールの指示に従ってブラウザで該当file IDを取得します。独自Pythonダウンローダーはありません。

TrueNASでは別のCustom Appで同等のread-only mountと新しい/data領域を使えます。既存composeの原本は本人が添付済みですが、この実行環境に取得済み原本はありませんでした。正本の正式転送はリンク更新後も取得を拒否され、原文を確認できていません。再添付が必要という判断にはせず、既存service名・host pathは未確認として保持しています。したがって既存composeへの確定差分とは表示しません。もし従来の`TYPE=CURSEFORGE`/`CF_SERVER_MOD`方式なら、導入方式の変更は`TYPE=AUTO_CURSEFORGE`、`CF_MODPACK_ZIP`へのZIPパス指定、`CF_SLUG`、同梱Composeの除外・保持3変数の移植、およびZIPとdownloadsのread-only mount追加です。従来の`CF_SERVER_MOD`は外します。変数の正確な189 IDの列は生成したComposeからそのまま使い、手入力で作り直しません。既存のport・memory・world領域の移行を自動では行いません。既存サービスのパス・world・composeを上書きしません。EULAは本人が確認して明示設定します。このZIPをCurseForge AppにImportするだけでサーバーが起動するという案内はしません。実機動作は本人が確認する範囲で、Docker/Javaの起動試験は実施していません。

### client 199件からserver 189件を選ぶ仕組み

App manifestのprojectID/fileID 199組を保持します。検証済み`exports/server.refs.json`は、その同じfile IDを持つ189組の部分集合です。差分10 project IDを`CF_EXCLUDE_MODS`へ渡し、189 project IDを`CF_FORCE_INCLUDE_MODS`へ渡します。`CF_EXCLUDE_INCLUDE_FILE`を空にしてイメージ同梱の別の除外規則は使いません。このため、参照の版を編集せずserver側の取得対象を指定できます。`SERVER-REFERENCES.json`自体を標準ツールのmanifestとして読ませる方式ではありません。標準ツールが読むのは`CF_MODPACK_ZIP`内の元manifestです。自動取得を許可しないファイルは標準ツールが不足を報告するため、指定された正確なfile IDをブラウザで取得してdownloadsへ置きます。実際の取得・起動結果は静的検査と区別します。

### 新規導入と既存ワールド移行

新規導入は別の空/data領域を用意し、manifestからloader・MODを取得、ZIPのoverridesを配置する手順です。既存ワールドを含まないので、最初に新規ワールドが生成されても既存ワールドの移行成功を意味しません。

既存ワールドを移す場合は、実際の旧起動ディレクトリと`level-name`を確認し、停止したサーバーの整合性あるコピーまたはスナップショットを別の/data領域で使います。worldと運用設定はローカルで保持し、MOD・loaderの旧実行ファイルは持ち越さずmanifestから導入します。`server.properties`、whitelist等の運用設定はZIPに含めず、必要な値を移行先へ引き継ぎます。秘密設定はREADMEや配布ZIPへ載せません。overridesのconfigは導入時に適用されるため、既存の運用設定と配布設定の差分を確認します。

[従来の`TYPE=CURSEFORGE`の公式仕様](https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/mod-platforms/curseforge/)では既定の`CF_BASE_DIR=/data/FeedTheBeast`等を作業場所にします。`AUTO_CURSEFORGE`は/dataへ導入するため、TYPEだけ変更して旧worldがそのまま見つかるとは扱いません。旧作業場所の正しいworldを新しい導入先に対応させる必要があります。今回、本番のcompose・world・設定には変更していません。実機確認は本人担当のままで、追加の実行承認や試験依頼はしません。

[公式Server Packガイド](https://blog.curseforge.com/server-packs-tutorial/)に従い対応clientのAdditional Fileへ紐づける提出metadataを用意します。ただし公式資料にこの導入用レイアウトの受理保証はなく、manifest形式のServer Packを一律禁止する記述も確認できていません。Appで出力したclientと、自動生成したサーバー導入用ZIPを区別して表示します。審査結果は実際の提出後に確認する必要があります。

## ライセンスと共通処理

本人指定の作者はShimaeです。自作の設定寄与・スクリプト・説明文はMITとし、LICENSEとLICENSE-SCOPE.txtで範囲を定めます。第三者Mod・Shader・ライブラリ・生成された既定設定やコメントの権利は各作者のままです。

空のApp authorと正規のshaderリンクへの既存対応を維持します。`reviewed_comments.json`のパスと行SHAが完全一致する説明コメントだけ接続先検査を除外し、認証値検査はその行にも適用します。

共通処理は`aiagate/minecraft-modpack-release`のcommit `e7e0fbd0e7dc405d21e8bb44fe4282a3651ac15a`を土台にしています。他パックのMOD構成・Secret・project IDは引き継ぎません。

- [Upload API](https://support.curseforge.com/support/solutions/articles/9000197321-curseforge-api)
- [正式Exportの手順](https://support.curseforge.com/support/solutions/articles/9000198500-exporting-a-modpack-for-curseforge-project-submission)
- [App Export / Import](https://support.curseforge.com/support/solutions/articles/9000198501-exporting-and-importing-modpacks)
- [Server Packガイド](https://blog.curseforge.com/server-packs-tutorial/)

## 0.0.1の登録状況

原本は732,350 bytes、SHA256 `042de1c25ce9995f04eac015ba9e6db257749a677c5ad02f50293b5decac7cf8`です。提出候補は430,127 bytes、SHA256 `b27742177d000e581a6b9ea0bd1540929ac291018ab70ef11f9bd1193dacd81c`です。公開する版はmanifestどおり`0.0.1`で、独自に`0.1-no-tfc`へ戻しません。

新しいApp出力の設定差分14件を保持し、追加された有効な設定3件も採用しました。未出力のシェーダー設定ファイルは勝手に追加しません。Apotheosis設定にあるPlacebo CFG仕様とEvalEx利用例への公開コメント2種類を、パスと行SHAに限定してレビュー済み例外へ登録しました。秘密値検査は常に適用します。実際の起動・掲載承認状態・CurseForge審査通過をこのローカル検査だけで証明したとは扱いません。

NeoForgeのmanifest処理は[公式インストーラー実装](https://github.com/itzg/mc-image-helper/blob/main/src/main/java/me/itzg/helpers/curseforge/CurseForgeInstaller.java)の`prepareModLoader`/`prepareNeoForge`でも確認しました。これは対象MOD一式の実機動作の保証ではありません。
