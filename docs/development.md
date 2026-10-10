# 開発・ビルド手順

通常のビルド入力は `pack/` です。MOD は project ID / file ID を固定して管理し、最新版への自動更新は行いません。

## 編集するファイル

- `pack/release.json`：版、ゲーム/loader、公開種別。
- `pack/client.refs.json`：clientのprojectID/fileID。日常のMOD更新はfile IDを明示してレビューします。自動で最新版へ更新しません。
- `pack/server.refs.json`：serverで使うclientの部分集合。同じprojectのfile IDはclientと一致させます。
- `pack/overrides/`：配布する設定・ライセンス文書。world、接続先、パスワード、履歴を入れません。
- `CHANGELOG.md`：リリースごとの追加機能・変更内容。

`pack/migration.json` は初回移行時の固定参照・設定SHAを記録し、移行版の内容照合に使用します。

## 生成方式

packwizは`v0.0.0-20260218225342-dfd8b68a4796`、Goは1.27.2で固定し、コンパイラーと本体module checksumを検証します。固定CF参照だけを一時的なpackwiz export入力へ変換します。この一時メタデータはCF export専用です。依存の自動追加、MOD取得、アップデート、Minecraft実行はしません。export自体はAPIキー不要・オフラインです。

標準toolが新しくmanifestとmodlistを生成します。App原本のmanifestをJSON置換しません。生成後はentry本文を変えず、順序・時刻・属性を固定した無圧縮ZIPへ再包装します。 packwizのMOD列挙順序は再実行で変わるため、再ビルドのZIPハッシュ一致は保証しません。CIではMOD参照・設定の内容一致を検証し、提出は同じ実行で保存した成果物のハッシュを照合します。受理済み版の再ビルドは別のZIPとして停止し、二重提出しません。client manifest version、表示版、出力名、タグは`pack/release.json`の版に揃えます。既存App originを新しいtool生成ZIPの出所として表示しません。

## 検証と CI

ローカル検証は `python3 -m unittest discover -s tests -v`。固定packwizを用意し、`python3 scripts/native_pack.py --output <新しい出力先> --packwiz <binary>`で両ZIPを生成します。CIは同じビルドを独立に2回実行し、参照と設定の内容一致を確認してレビュー用artifactを保存します。実提出を伴わないCIにUpload tokenは渡しません。

Actions の表示名は `CI / Validate`、`Release / Submit`、`Release / Verify publication` です。Validate は main への push と PR で実行し、同じ PR・ブランチの古い検証はキャンセルします。テスト、固定 Go / packwiz の準備、配布バイナリの混入検査、ZIP 生成・検証は `.github/actions/build-pack/action.yml` にまとめ、Validate と Submit の preflight で共有します。独立した再ビルド比較は Validate で行います。Submit は同じ run で生成した ZIP を Environment の承認後に提出し、成功した提出 job の後だけ公開確認を呼び出します。提出前の GET audit は Submit 内で実行します。

Gitには配布ZIP・MOD JAR・私的な運用資料を入れません。公開済みRelease/ZIP、App原本、監査receipt、ローカル運用資料はcleanupの対象外です。

コマンドはリポジトリのルートで実行します。固定 packwiz の用意は `.github/actions/build-pack/action.yml` を参照してください。配布物の導入は [サーバー導入手順](server-setup.md)、提出は [公開手順](publishing.md)で扱います。
