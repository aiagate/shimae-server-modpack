# Shimae Server Modpack

Minecraft 1.21.1 向けの Modpack です。クライアント用の CurseForge manifest ZIP と、Docker で導入する Server Pack を配布します。

上書き更新や既存ワールドの移行を行う場合は、事前にワールドをバックアップしたうえで、[変更履歴](CHANGELOG.md)（廃止・置換された旧 MOD JAR の退避など版ごとの注意点）を参照してください。

## ダウンロードと導入

配布先は [GitHub Releases](https://github.com/aiagate/shimae-server-modpack/releases) と [CurseForge](https://www.curseforge.com/minecraft/modpacks/shimae-server-modpack/files)（project ID `1733082`）です。

クライアントには `shimae-server-modpack-<version>.zip` を使用します。CurseForge App で ZIP をインポートし、MOD の取得後に起動してください。サーバーには同じ版のクライアントで接続します。

サーバーには `shimae-server-modpack-<version>-serverpack.zip` を使用します。この ZIP は導入用で、MOD JAR や Java を同梱した起動可能なサーバー一式ではありません。導入手順は ZIP 内の `README-SERVER.md` を参照してください。

## 配布内容

| 項目 | 内容 |
| --- | --- |
| Minecraft / loader | 1.21.1 / NeoForge（正確なローダー版は [pack/release.json](pack/release.json) および各リリースの manifest を参照） |
| クライアント | 固定 MOD 参照（[pack/client.refs.json](pack/client.refs.json)）、設定、ライセンス文書 |
| サーバー | サーバー用 MOD 参照（[pack/server.refs.json](pack/server.refs.json)）、設定、ライセンス文書、Compose と導入手順 |

配布 ZIP に MOD JAR、world、接続先、認証情報は含めません。サーバーの manifest はクライアントと同一で、Compose がクライアント専用 MOD を除外します。

## 開発

[uv](https://docs.astral.sh/uv/getting-started/installation/) をインストールし、リポジトリのルートで実行してください。uv が Python 3.14 と仮想環境を用意します。

```sh
uv sync --locked
uv run --locked python -m unittest discover -s tests -v
uv run --locked python -m compileall -q scripts tests
```

配布 ZIP をローカルで生成するには、CI と同じ版の packwiz を用意し、未作成の出力先を指定します。

```sh
uv run --locked python scripts/native_pack.py --output ./build --packwiz /path/to/packwiz
```

## ライセンス

自作の設定への寄与、スクリプト、文書には [MIT License](LICENSE) を適用します。第三者の MOD、Shader、ライブラリ、生成された設定本文やコメントの権利は各作者に帰属します。適用範囲と配布物内の通知は [THIRD-PARTY-NOTICES.txt](pack/overrides/THIRD-PARTY-NOTICES.txt)を参照してください。
