# Shimae Server Modpack

Minecraft 1.21.1 / NeoForge 21.1.243 向けの Modpack です。クライアント用の CurseForge manifest ZIP と、Docker で導入する Server Pack を配布します。

## ダウンロードと導入

公開済みの 0.0.2 は [GitHub Release](https://github.com/aiagate/shimae-server-modpack/releases/tag/v0.0.2) から取得できます。CurseForge project ID は `1733082`、client file ID は `9104708`、server file ID は `9104783` です。公開時の根拠は [0.0.2 の提出記録](CHANGELOG.md#002-submission-evidence)にあります。

クライアントには `shimae-server-modpack-0.0.2.zip` を使用します。CurseForge App で ZIP をインポートし、MOD の取得後に起動してください。サーバーには同じ版のクライアントで接続します。

サーバーには `shimae-server-modpack-0.0.2-serverpack.zip` を使用します。この ZIP は導入用で、MOD JAR や Java を同梱した起動可能なサーバー一式ではありません。[サーバー導入手順](docs/server-setup.md)と ZIP 内の `README-SERVER.md` を参照してください。

## 配布内容と動作確認の範囲

| 項目 | 0.0.2 の内容 |
| --- | --- |
| Minecraft / loader | 1.21.1 / NeoForge 21.1.243 |
| クライアント | 固定参照 199 件、設定 318 ファイル、ライセンス文書 2 件 |
| サーバー | サーバー用参照 189 件、設定 309 ファイル、ライセンス文書、Compose と導入手順 |

配布 ZIP に MOD JAR、world、接続先、認証情報は含めません。サーバーの manifest はクライアントと同一で、Compose がクライアント専用の 10 project ID を除外します。

参照・設定の静的検査と、公開ファイルの親子関係・Server Pack 区分・SHA256 の検証を行っています。この導入方式の実機起動試験は未実施です。全 MOD の依存関係や実行時の互換性を保証するものではありません。

## 0.0.3 の更新候補

Minecraft / NeoForge を維持し、クライアントの 88 参照（サーバー共通 84 参照）を更新します。2026-10-10 に本人からローカルクライアントの起動成功の報告を受けました。ワールド読み込み・移行・専用サーバー起動は未確認です。固定 file ID、依存検査と保留理由は[更新レビュー](docs/mod-update-0.0.3.md)を参照してください。

## 文書の案内

- [CHANGELOG.md](CHANGELOG.md)：版ごとの変更内容。
- [サーバー導入手順](docs/server-setup.md)：新規導入と既存 world の移行。
- [開発・ビルド手順](docs/development.md)：編集対象、固定ツール、ローカル検証、CI。
- [公開手順](docs/publishing.md)：提出、審査、区分設定、公開確認。
- [CHANGELOG の履歴資料](CHANGELOG.md#001-app-migration-evidence)：過去の提出・移行の根拠資料。

## ライセンス

自作の設定への寄与、スクリプト、文書には [MIT License](LICENSE) を適用します。第三者の MOD、Shader、ライブラリ、生成された設定本文やコメントの権利は各作者に帰属します。適用範囲と配布物内の通知は [THIRD-PARTY-NOTICES.txt](pack/overrides/THIRD-PARTY-NOTICES.txt)を参照してください。
