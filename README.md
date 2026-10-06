# Shimae Server Modpack

`aiagate/shimae-server-modpack` は **Shimae Server Modpack** のリリース管理用リポジトリです。表示名は `Shimae Server Modpack`、slug・配布ファイル名の基本は `shimae-server-modpack` に揃えます。

**初期雛形です。MOD構成、Minecraft/loaderの版、author、CurseForge project ID、正式App exportは未指定です。** 他のパックの20MOD構成や動作確認、asset ID、ハッシュ、作者、Secretsをこのパックの設定として引き継いでいません。取込ZIPの生成・公開・ダウンロードはまだできません。専用サーバーを実行するZIPも収録しません。共通処理はクライアント用App exportの提出を扱い、サーバーパック提出は扱いません。

## 初期状態とCI

- push/PRのValidateはテスト、Python構文、GitへのZIP混入を確認します。MODをダウンロード・実行せず、配布ZIPやartifactを生成しません。
- `release.example.json` のIDはnull、版とレビュー済みSHA256は未設定です。実設定の `release.json` はまだありません。例をそのままコピーしても取得・提出はネットワーク接続前に停止します。
- Manual CurseForge submissionはmainの `workflow_dispatch` だけです。既定は取得・検査のみで、設定がない初期状態ではpreflightが失敗し、提出jobへ進みません。
- `curseforge` environment、提出Token、有効化Variableは作成・設定していません。テストは合成fixtureで、実MOD構成やApp exportの検証済み主張ではありません。

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
```

## 正式な構成を用意する

1. Minecraft/loaderの版、収録MODと配布条件、クライアント用途を決め、別の配布専用CurseForge Appプロフィールを作ります。名前をShimae Server Modpackとし、正式な版と本人指定のauthorをApp上で設定します。名前からサーバー実行パックと誤解されないよう目的を記載します。
2. Appで起動と必要なサーバー参加を確認し、配布に必要なファイルだけexportします。生成manifestは手編集しません。修正が必要ならAppプロフィールを直して再exportします。
3. 外部へ載せる前に全内容を人が確認します。ワールド、ログ、options.txt、servers.dat、私的config、サーバー接続先、個人の地図、認証情報を除きます。未レビューのZIPは手元の非共有フォルダだけに置きます。jar再配布の権利も確認します。
4. CurseForgeでこのパック専用のprojectを作り、実project IDを確認します。別パックのproject IDを使いません。`cp release.example.json release.json` で設定を作り、exportからMinecraft版・loader ID・表示名・release typeを入力します。`game_version_names` はMinecraft版、対応Loader名、Clientです。
5. 全内容レビュー済みZIPのSHA256を `reviewed_sha256` に記入し、CHANGELOGを書きます。ローカル検査の `export_asset_id` はnullのまま使えます。

```bash
sha256sum /private/path/shimae-server-modpack.zip
python3 scripts/release.py --zip /private/path/shimae-server-modpack.zip
```

ローカル検査は既定で通信・提出をしません。停止理由をレビューし、ハッシュだけを書き換えて検査を省略しないでください。Windowsでは `Get-FileHash -Algorithm SHA256 <ZIPのパス>` でも確認できます。

## レビュー済みZIPの保管と取得

ローカル検査と人の全内容レビュー後、このリポジトリの公開Releaseへ正式exportをassetとして保存し、取得したasset IDを `release.json` の `export_asset_id` に記入します。名前だけで自動選択せず、IDとレビュー済みSHA256で固定します。設定とCHANGELOGをレビューしてmainへ反映した後、ActionsのManual CurseForge submissionを `submit=false` で実行して検査します。

**このリポジトリはpublicです。Release assetはCurseForge審査前でも誰でも取得できます。** レビュー前のZIPをGit、Release、Actions artifactに載せないでください。Gitではコード・設定・変更履歴だけを管理し、ZIPは追跡しません。過去のGit履歴に誤って含めた情報は、現在のファイルを削除しても消えません。

取得処理は認証なしGET、固定repo `aiagate/shimae-server-modpack` のasset API、許可したGitHub HTTPS配信先、圧縮90 MiBの上限に制限します。SHA256・ZIP構造・内容検査が通るまでZIPを保存しません。preflightは検査済みZIPとreceiptを30日保持のartifactに保存し、同じrunの正確なArtifact IDと同じcommitの設定で提出jobへ渡します。

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
