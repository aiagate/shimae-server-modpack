# 開発・ビルド手順

通常のビルド入力は `pack/` です。MOD は project ID / file ID を固定して管理し、最新版への自動更新は行いません。

## 編集するファイル

- `pack/release.json`：版、ゲーム/loader、公開種別。現在は 0.0.2。
- `pack/client.refs.json`：clientのprojectID/fileID。日常のMOD更新はfile IDを明示してレビューします。自動で最新版へ更新しません。
- `pack/server.refs.json`：serverで使うclientの部分集合。同じprojectのfile IDはclientと一致させます。
- `pack/overrides/`：配布する設定・ライセンス文書。world、接続先、パスワード、履歴を入れません。
- `CHANGELOG.md`：今回の変更、導入方式、動作確認の範囲。

0.0.2への移行ではclient199参照、server189参照、client override320ファイル（設定318＋ライセンス2）、server設定309を保持しています。App由来0.0.1の固定参照・設定SHAと完全照合します。旧 App の出所・設定ポリシー・準備記録は [CHANGELOG](../CHANGELOG.md#001-app-migration-evidence) に統合されています。元の JSON は同節の固定 Git snapshot に保持し、通常ビルドでは参照しません。初回移行の参照・設定SHAは`pack/migration.json`で照合します。

## 生成方式

packwizは`v0.0.0-20260218225342-dfd8b68a4796`、Goは1.27.2で固定し、コンパイラーと本体module checksumを検証します。固定CF参照だけを一時的なpackwiz export入力へ変換します。これはCF export専用で、packwiz-installer向けのMODハッシュを捏造しません。依存の自動追加、MOD取得、アップデート、Minecraft実行はしません。export自体はAPIキー不要・オフラインです。

標準toolが新しくmanifestとmodlistを生成します。App原本のmanifestをJSON置換しません。生成後はentry本文を変えず、順序・時刻・属性を固定した無圧縮ZIPへ再包装します。 packwizのMOD列挙順序は再実行で変わるため、再ビルドのZIPハッシュ一致は保証しません。CIではMOD参照・設定の内容一致を検証し、提出は同じ実行で保存した成果物のハッシュを照合します。受理済み版の再ビルドは別のZIPとして停止し、二重提出しません。client manifest version、表示版、出力名、タグは`pack/release.json`の版に揃えます。既存App originを新しいtool生成ZIPの出所として表示しません。

## 検証と CI

ローカル検証は `python3 -m unittest discover -s tests -v`。固定packwizを用意し、`python3 scripts/native_pack.py --output <新しい出力先> --packwiz <binary>`で両ZIPを生成します。CIは同じビルドを独立に2回実行し、参照と設定の内容一致を確認してレビュー用artifactを保存します。実提出を伴わないCIにUpload tokenは渡しません。

[0.0.2 の提出記録](../CHANGELOG.md#002-submission-evidence)に公開済み版の受付ID・SHA・回復経緯を記録しています。完了した0.0.2専用の回復操作は退役しました。現行の`server_only`、公開済み親のバイト照合、immutable claim/result、失敗receiptは保持しています。受付不明のclaimがあれば再送せず、作者画面とreceiptを確認します。

Gitには配布ZIP・MOD JAR・私的な運用資料を入れません。公開済みRelease/ZIP、App原本、監査receipt、ローカル運用資料はcleanupの対象外です。

コマンドはリポジトリのルートで実行します。固定 packwiz の用意は `.github/workflows/validate.yml` を参照してください。配布物の導入は [サーバー導入手順](server-setup.md)、提出は [公開手順](publishing.md)で扱います。
