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

## Actionsから正式公開まで

`validate.yml`はpush/PRでfixtureテスト、Python構文、GitのZIP混入、client入力状態を検査します。入力待ちは明示して取得をスキップします。client入力が揃えば固定assetのZIPを検査します。serverのasset・SHA・出所が未設定でもclientの検査は進められます。PRではartifactを保存しません。

`submit.yml`はmainからの手動起動のみです。`submit=false`でclient ZIPを取得・検査し、投稿メタデータとCHANGELOGも確認します。検査済みclient ZIPを単独artifact、SHA256SUMSとreceiptを別artifactとして14日保存します。server artifactは必須にしません。

`submit=true`では既存`curseforge` Environmentを利用して、同じrunのclient artifact IDだけを固定して取得します。`skip-decompress:true`で元ZIPを展開せず、同じcommitの設定とSHAを再検査し、同じバイトを一度だけUpload APIへPOSTします。API受付は審査・公開完了とは区別します。受付不明時は作者画面で確認し、自動再送しません。

提出失敗のreceiptにはHTTP status、固定のエラー分類、処理段階だけを記録します。HTTP拒否、TLS・通信・timeout・HTTP protocol異常、不正JSON・file ID欠落等を区別し、応答本文・認証ヘッダー・例外の生の文字列は記録しません。失敗時の受付状態は引き続き未確認とし、診断分類だけを根拠に再提出しません。

既存Secret `CURSEFORGE_API_TOKEN`、Variable `CURSEFORGE_SUBMISSION_ENABLED=true`、workflowのmain限定・手動起動を利用します。Environmentの保護ルールは現在ありません。このローカル修正でSecretや権限を設定しません。Token値はチャット・Git・コマンド引数・ログへ載せません。

公開までには、修正のPR反映・CI・レビューとマージ、正本asset登録、手動検査とclient提出、CurseForge審査と作者画面での手動公開が必要です。完了はCurseForgeで利用者がインストールできる公開状態を確認して判断します。Git入力・Release・artifactが公開される運用は本人確認済みです。

## 検査の範囲と生成案

ZIPのCRC、SHA256、manifest・版・loader・参照ID、危険なパス、重複、symlink、暗号化、サイズ、実行属性、設定の秘密値・私的接続先・不要状態、JSON/TOMLを検査します。参照件数だけで合格にせず、199参照の完全lockと照合します。MODの全依存グラフ、mixins、掲載承認状態、実機動作や配布権利を完全自動証明したとは扱いません。

`exports/server.refs.json`とserver側のpolicyは構成比較用の既存メタデータです。これはserver ZIPの受領を要求するものではありません。server用の取込プロフィールはJAR入りの実行Server PackとしてAdditional Fileへ投稿しません。

[公式審査規約](https://support.curseforge.com/support/solutions/articles/9000197279-project-and-modpack-moderation-policies)はAppでのModPack作成とApp生成manifestの編集禁止を明記しています。独自の互換ZIP生成はApp起源の証拠になりません。独自生成のローカル修正は別に保持し、今回の正式投稿フローへ混ぜません。

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
