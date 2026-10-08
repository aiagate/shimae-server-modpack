# Shimae Server Modpack

`aiagate/shimae-server-modpack` は **Shimae Server Modpack** のリリース管理用リポジトリです。表示名は `Shimae Server Modpack`、slug・配布ファイル名の基本は `shimae-server-modpack` に揃えます。

CurseForge project IDは`1733082`、対象はMinecraft `1.21.1` / NeoForge `21.1.243`です。**正式な未改変App Exportは未受領で、取得・提出は入力待ちです。** 既存のローカル編集した取込ZIPをApp出力として登録しません。ActionsはAppを操作せず、manifest生成・ZIP再構築・設定の自動修正も行いません。

## 初期状態とCI

- push/PRのValidateはテスト、Python構文、GitへのZIP混入、App Export入力状態を確認します。入力待ちは明示してZIP取得をスキップし、正式入力が揃ったときは固定assetの2ZIPを検査します。PRではartifactを保存しません。MODのダウンロード・実行は行いません。
- `release.json`にproject ID `1733082`とゲーム版を設定しました。正式版、client asset ID、SHA256は未設定です。`exports/exports.lock.json`の両App出力も未確認のため、手動preflightはネットワーク接続前に`INPUT_WAIT`で停止します。汎用の`release.example.json`は未設定の例として残します。
- Manual CurseForge submissionはmainの `workflow_dispatch` だけです。既定は取得・検査のみで、正式App Export未受領の状態ではpreflightが失敗し、提出jobへ進みません。
- `curseforge` environment、提出Token、有効化Variableは作成・設定していません。テストは合成fixtureで、実MOD構成やApp exportの検証済み主張ではありません。

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
```

## 正式な構成を用意する

1. Minecraft/loaderの版、収録MODと配布条件、クライアント用途を決め、別の配布専用CurseForge Appプロフィールを作ります。名前をShimae Server Modpackとし、正式な版と本人指定のauthorをApp上で設定します。名前からサーバー実行パックと誤解されないよう目的を記載します。
2. Appで起動と必要なサーバー参加を確認し、配布に必要なファイルだけexportします。生成manifestは手編集しません。修正が必要ならAppプロフィールを直して再exportします。
3. 外部へ載せる前に全内容を人が確認します。ワールド、ログ、options.txt、servers.dat、私的config、サーバー接続先、個人の地図、認証情報を除きます。未レビューのZIPは手元の非共有フォルダだけに置きます。jar再配布の権利も確認します。
4. 本パックの専用project ID `1733082`を使います。既存`release.json`へApp Export由来の正式版・表示名・client asset ID・SHA256を入力します。`game_version_names`はMinecraft版、対応Loader名、Clientです。
5. 全内容レビュー済みZIPのSHA256を `reviewed_sha256` に記入し、CHANGELOGを書きます。ローカル検査の `export_asset_id` はnullのまま使えます。

```bash
sha256sum /private/path/shimae-server-modpack.zip
python3 scripts/release.py --zip /private/path/shimae-server-modpack.zip
```

ローカル検査は既定で通信・提出をしません。停止理由をレビューし、ハッシュだけを書き換えて検査を省略しないでください。Windowsでは `Get-FileHash -Algorithm SHA256 <ZIPのパス>` でも確認できます。

## レビュー済みZIPの保管と取得

ローカル検査と人の全内容レビュー後、このリポジトリの公開Releaseへ正式exportをassetとして保存し、取得したasset IDを `release.json` の `export_asset_id` に記入します。名前だけで自動選択せず、IDとレビュー済みSHA256で固定します。設定とCHANGELOGをレビューしてmainへ反映した後、ActionsのManual CurseForge submissionを `submit=false` で実行して検査します。

**このリポジトリはpublicです。Release assetはCurseForge審査前でも誰でも取得できます。** レビュー前のZIPをGit、Release、Actions artifactに載せないでください。Gitではコード・設定・変更履歴だけを管理し、ZIPは追跡しません。過去のGit履歴に誤って含めた情報は、現在のファイルを削除しても消えません。

取得処理は認証なしGET、固定repo `aiagate/shimae-server-modpack` のasset API、許可したGitHub HTTPS配信先、圧縮90 MiBの上限に制限します。SHA256・ZIP構造・内容検査が通るまでZIPを保存しません。preflightは検査済み2ZIPをそれぞれ未改変の単独artifactへ、SHA256SUMSとreceiptを別artifactへ保存します。保持14日です。提出jobへはclientの正確なartifact IDだけを渡します。download-artifact v8の`skip-decompress:true`で元のZIPを展開せず取得し、同じcommitの設定とSHAを再検査します。

## 提出を有効化するとき

設定・正式export・検査が整ってから、ユーザーがGitHubのEnvironment `curseforge` に必要な承認者とmain制限を設定し、Secret `CURSEFORGE_API_TOKEN` とVariable `CURSEFORGE_SUBMISSION_ENABLED=true` を設定します。TokenはCurseForgeの投稿用API tokenです。チャット、Git、コマンド引数、ログへ値を載せません。現時点では設定しません。

承認ゲートの利用可否を確認し、正式提出はActionsで `submit=true` を選びます。提出jobは再度SHA256と内容を検査し、同じバイトを `shimae-server-modpack.zip` というmultipartファイル名で一度だけPOSTします。ZIPの中身は改変しません。API受付とCurseForge審査・公開は別です。

receiptにはcommit、exportの版、ZIP SHA256、asset ID、project ID、受付file ID、状態（validated/submitted/submission_unconfirmed）を残します。タイムアウト・中断などでは受付済みの可能性があり、作者画面で確認するまで再実行しません。自動再送はなく、concurrencyは同時実行の直列化であり、手動再実行の重複を永続的に防ぐ機能ではありません。

## 検査の範囲

ZIPを展開せず、SHA256、manifest、版、loader、MOD参照、危険なパス、重複、symlink、暗号化、CRC、サイズを検査します。上限は圧縮90 MiB、展開256 MiB、1ファイル32 MiB、1万エントリ、圧縮率200倍というローカル方針です。正式App exportにはroot manifestとoverridesが必要です。草案版 `0.0.0-local.*` とREPLACEの仮identityは提出拒否します。

overridesは検査できるUTF-8テキストのみを許可し、jar・入れ子ZIP・バイナリ・私的ファイル・接続先らしい記述を拒否します。manifestとmodlist.htmlも検査します。App由来、任意の秘密値、配布許可、MODの互換性や動作は完全自動判定できないため、人の確認が必要です。

## 共通処理の出所と公式資料

取得・検査・提出処理は `aiagate/minecraft-modpack-release` の共通実装（commit `e7e0fbd0e7dc405d21e8bb44fe4282a3651ac15a`）を土台に、固定取得repoと名前をこのパック用に変更しました。元のプロフィール・MOD構成・生成草案・公開ZIPはコピーしていません。ここでのテスト成功はShimaeのMOD構成の動作確認を意味しません。

- [CurseForge Upload API](https://support.curseforge.com/support/solutions/articles/9000197321-curseforge-api)
- [正式提出ZIPの形式](https://support.curseforge.com/support/solutions/articles/9000198500-exporting-a-modpack-for-curseforge-project-submission)
- [審査規約](https://support.curseforge.com/support/solutions/articles/9000197279-project-and-modpack-moderation-policies)
- [Appのexport/import](https://support.curseforge.com/support/solutions/articles/9000198501-exporting-and-importing-modpacks)

初期公開ではMODの推測、ZIP配布、CurseForge実提出、Secret・権限設定を行いません。

## 2026-10-08のローカル準備

作者は本人指定のShimaeです。自作の設定寄与・リリーススクリプト・説明文はMITとし、LICENSEとLICENSE-SCOPE.txtで適用範囲を定めます。第三者Mod・Shader・ライブラリ・生成された既定設定やコメントの権利は各作者のままです。

公開区分は本人選択のReleaseですが、修正版ZIPでの実機起動・必要なサーバー接続の結果を確認するまで公開しません。以前の原App Exportは201参照でした。現行の構成比較基準はTFC除外後のclient199/server189参照であり、ローカル編集したZIPから採った基準です。新しい未改変App Exportの出所を証明するものではありません。公開設定やRelease assetを今回用意したという意味ではありません。

検査は正規CurseForgeの/minecraft/shaders/リンクを認めます。未知のサイト、URL userinfo/query、接続先や認証値を一律に許可しません。設定の説明コメントはscripts/reviewed_comments.jsonにレビュー済みのファイルパスと行SHA256を記録し、完全一致する#コメント行だけを接続先検査の例外にします。認証値検査は例外行にも適用します。コメントの変更・追加や別ファイルへの移動は再レビューが必要です。

App生成manifestのauthorが空でも、文字列であることを検査し、本人指定のproject attributionとは別に扱います。名前と版、仮identity/草案版の拒否は維持し、checkerを通すためのmanifest手編集はしません。

以前のローカル準備では不要な個人履歴・バックアップ等を整理した候補を作成しました。正式配布入力ではAppプロフィールとExport対象を事前に整理し、必要なライセンス文書もExport前に配置します。Export後のZIPを編集してcheckerを通す運用はしません。

正式入力は本人がAppからExportした未改変ZIPだけに限定します。不合格時はAppプロフィール側を修正して再Exportします。CurseForgeの審査適合・全参照fileIDの掲載承認/互換性・実機動作は、このローカル検査の成功だけでは保証できません。


## 2つのApp Exportを登録する

1. Appでclientとserver用プロフィールを確認します。client199/server189参照が基準で、TFC、Offset Smoker、Bonsaiは除外、PatchouliとApotheosis系列は保持します。serverはclientの部分集合で、共通File IDは同一です。差分10件は`exports/policy.json`に固定しています。
2. ベンチマーク、Sodium fingerprint、Chunkyの作業状態、未使用Bonsaiのclient/common設定、個人履歴等をExport前に除きます。有効なChunky設定`config/chunky/config.json`は保持します。ZIP内の許可テキストとSHAはpolicyの基準と照合し、Appの再Exportで差異が生じた場合は理由をレビューしてpolicyを更新します。
3. 2ZIPの版、manifest名、名前、サイズ、SHAとExport日・プロフィール名・確認者を`exports/exports.lock.json`へ登録します。`origin.confirmed=true`は人の確認記録です。機械はApp出所や配布権利を証明できません。
4. `exports/client.refs.json`と`server.refs.json`は構成比較の正本です。現在の基準との差分を確認し、App Exportの参照と完全一致させます。許可overrideのハッシュも比較します。自動的な参照書き換えはしません。
5. 本リポジトリのReleaseへ2ZIPを保存し、asset IDをlockに固定します。`release.json`のclient asset ID/SHAも同一にします。版・表示名・CHANGELOGを確定してmainへ反映し、`submit=false`で取得・検査を確認します。

ローカル検査はネットワーク・投稿なしで実施できます。公開前のローカル検査では両asset IDと`release.json`のasset IDをnullのまま使えます。公開後は実際のasset IDを固定します。予定値や仮IDでは取得しません。

```bash
python3 scripts/verify_app_exports.py --check-state
python3 scripts/verify_app_exports.py --client /path/client-app-export.zip --server /path/server-app-export.zip
```

入力待ちのPRはfixtureテストと構成基準の検査だけを通過します。これは実ZIPの検証完了ではありません。手動preflightは入力待ちのまま成功扱いにしません。

正式投稿は`submit=true`でclientだけを扱います。server用App ExportはMOD参照型の取込補助ZIPとしてGitHubで保存し、実行用Server PackとしてCurseForgeへ投稿しません。[公式Server Packガイド](https://blog.curseforge.com/server-packs-tutorial/)は`mods`・`config`を含む実行用ZIPを親ファイルのAdditional Fileとして登録する工程を示しています。

今回の連携に必要な本人の設定は、投稿権限のあるCurseForge upload tokenをGitHub `curseforge` EnvironmentのSecret `CURSEFORGE_API_TOKEN`へ直接登録すること、同EnvironmentのVariable `CURSEFORGE_SUBMISSION_ENABLED=true`、main制限と利用可能な承認ゲートです。値はチャット・Git・コマンド引数・ログへ書きません。API受付後は作者画面で審査・手動公開を確認します。
