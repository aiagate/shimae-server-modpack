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
uv run --locked ruff check scripts tests
uv run --locked ty check
uv run --locked python -m unittest discover -s tests -v
```

配布 ZIP をローカルで生成するには、CI と同じ版の packwiz を用意し、未作成の出力先を指定します。

```sh
uv run --locked python scripts/build_pack.py --output ./build --packwiz /path/to/packwiz
```

### MOD依存バージョンのLint

Validate と Submit の preflight は、`ci/mod-dependencies.json` に保存した固定ファイルのメタデータを、クライアント／サーバー別に照合します。NeoForge の宣言範囲を Maven の版比較で判定し、導入済みの任意依存の範囲違反も停止します。Minecraft は起動せず、CI で各 MOD を再ダウンロードしません。

MOD の固定参照を追加・更新するときは、CurseForge から**指定ファイルIDの実ファイル**を取得し、作業用ディレクトリに `<projectID>-<fileID>.jar`（シェーダーは `.zip`）として置きます。refs を更新した後、`uv run --locked python scripts/dependency_lint.py --refresh <作業用ディレクトリ>` を実行し、生成されたロックの差分も PR に含めます。変更のないファイルは再取得不要です。削除のみの変更では空のディレクトリを渡せます。未収録の固定ファイルがあると CI は停止します。JAR 本体はコミットしません。

対象は外側の MOD が宣言した版条件です。同梱 JAR は依存先候補として読み、候補のどれがロードされるかで結論が変わる場合や、静的に依存先を特定できない場合は未確定と表示します。ゲーム内動作やワールド移行はこのチェックの対象外です。

## ライセンス

自作の設定への寄与、スクリプト、文書には [MIT License](LICENSE) を適用します。第三者の MOD、Shader、ライブラリ、生成された設定本文やコメントの権利は各作者に帰属します。適用範囲と配布物内の通知は [THIRD-PARTY-NOTICES.txt](pack/overrides/THIRD-PARTY-NOTICES.txt)を参照してください。

## TFMG を含むワールドの移行

TFMG 1.2.0 に由来する自然生成ブロックの置換先は [tfmg-worldgen.json](pack/overrides/config/remapids/remaps/tfmg-worldgen.json) を参照してください。TFMG の [1.2.0 ソース](https://github.com/DrMango14/Create-The_Factory_Must_Grow/tree/e55d31525382ba7106a82ee5db90c7a2571f87ca) の鉱床データと油田・油井の生成コードをもとにしています。

パックにはクライアント・サーバー両方に [Remap IDs 2.1.0](https://www.curseforge.com/minecraft/mc-mods/remap-ids/files/8638635) と置換設定が入ります。サーバー停止中にワールドをバックアップし、更新後の構成でコピーを開いてください。上書き導入では、旧 TFMG とその Sable 連携、Tracks+、旧 Bits ’n’ Bobs の JAR を先に退避します。

置換は各チャンクの読み込み時に適用され、チャンクが保存されると置換先の ID が記録されます。未ロードのチャンクにも適用できるよう、生成済みチャンクの移行が済むまでは Remap IDs と置換設定を使用してください。

置換はブロック ID 単位です。オーバーワールドとネザーに共通する Fireclay や、地表にも出る原油ブロックには同じ置換先を使います。原油は石に変わるため、地表の油だまりも石になります。リストは自然生成されたブロックを対象とし、TFMG の機械、アイテム、ブロックエンティティのデータは移行対象外です。
