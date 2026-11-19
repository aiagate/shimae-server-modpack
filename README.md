# Shimae Server Modpack

Minecraft 1.21.1 向けの Modpack です。クライアント用の CurseForge manifest ZIP と、Docker で導入する Server Pack を配布します。

正式版 `0.0.8` は検証候補の構成で、正式0.0.7（client 206 / server 193参照）を基点に、Create: Tracks 1.0.1 を Create: Tracks+ 1.0.6b7 へ置換し、Items Displayed 2.0.10、Create: Ornithopter Glider 1.2.1、Better Days 3.3.6.3、Streams Reflowing 2.17.5、Clutter No More 3.1.3 をclient/server両側へ追加します。Minecraft 1.21.1 / NeoForge 21.1.266、client 211 / server 198の固定参照です。New Year's Delightは newYear mode をOFFに固定し、Better Daysは昼25分・夜15分を指定します。既存のCreate各種・DH・Iris・LAMB設定は維持しています。[追加MODと検証範囲](docs/mod-additions-0.0.8.md)を参照してください。

0.0.8の追加・置換6件はCurseForgeの固定ファイルを確認済みです。ただし**実機同居テスト・client GUI・本番world移行は未検証**です。Contraption Lightsは `LAMB` 方式で、shaderpack使用中の色光には制約があります。

0.0.7から移行する場合は、停止後に両側の実modsフォルダから旧JAR `tracks-neoforge-1.21.1-1.0.1.jar` を退避してください（mod IDが同一のため旧JARの残存は二重読込になります）。既存 `config/tracks-server.toml`・DH設定・world・キャッシュは保持してください。0.0.5以前からの移行はChunky、Create Stats、VSSの旧JARを残さないでください。Create Statsのコンテンツは提供元を失うため、worldをバックアップし隔離コピーで確認してください。NASの既存Composeと実効loaderの読み戻し・変更はこのリリース作業では行っていません。

## ダウンロードと導入

正式0.0.8の配布先は [GitHub Release](https://github.com/aiagate/shimae-server-modpack/releases/tag/v0.0.8) と [CurseForge](https://www.curseforge.com/minecraft/modpacks/shimae-server-modpack/files)（project ID `1733082`）です。CurseForgeの審査状況・受付IDはActionsの公開検証receiptで確認できます。

クライアントには `shimae-server-modpack-0.0.8.zip` を使用します。CurseForge App で ZIP をインポートし、MOD の取得後に起動してください。サーバーには同じ版のクライアントで接続します。

サーバーには `shimae-server-modpack-0.0.8-serverpack.zip` を使用します。この ZIP は導入用で、MOD JAR や Java を同梱した起動可能なサーバー一式ではありません。[サーバー導入手順](docs/server-setup.md)と ZIP 内の `README-SERVER.md` を参照してください。

## 配布内容

| 項目 | 0.0.8 の内容 |
| --- | --- |
| Minecraft / loader | 1.21.1 / NeoForge 21.1.266 |
| クライアント | 固定参照 211 件、設定、ライセンス文書 |
| サーバー | サーバー用参照 198 件、設定、ライセンス文書、Compose と導入手順 |

配布 ZIP に MOD JAR、world、接続先、認証情報は含めません。サーバーの manifest はクライアントと同一で、Compose がクライアント専用の 13 project ID を除外します。

## 0.0.5 の修正内容

Thirst Was Taken 2.1.5 を Thirst Was Reclaimed 3.0.6 に置換し、Jade 15.10.6 の流体表示で発生する既知の Mixin 競合を除去します。クライアント・サーバーを同じ版に揃え、旧 Thirst と併用しないでください。Aero などの他 MOD の固定参照は変更しません。ドッキングコネクタの実機再現は未実施です。[検証記録](docs/thirst-fix-0.0.5.md)を参照してください。

## 0.0.4 の更新内容

- Create: Design n' Decor 2.2b と Create Coasters 2.0 を追加。
- Coasters の3ブロックにサバイバル用レシピを追加し、全ワールドへ自動適用。
- JEI の検索対象を通常のCreativeタブに載らないアイテムにも拡張。

当時のMinecraft / NeoForgeは1.21.1 / 21.1.243です。クライアント 203／サーバー 193 件の固定MOD参照を使用します。[レシピの使い方](docs/coasters-recipes.md)と[変更履歴](CHANGELOG.md)を参照してください。公開版のダウンロード先は上記の案内を使用してください。

## 文書の案内

- [CHANGELOG.md](CHANGELOG.md)：版ごとの変更内容。
- [サーバー導入手順](docs/server-setup.md)：新規導入と既存 world の移行。
- [開発・ビルド手順](docs/development.md)：編集対象、固定ツール、ローカル検証、CI。
- [公開手順](docs/publishing.md)：提出、審査、区分設定、公開確認。
- [公開・移行の履歴資料](docs/release-history.md#001-app-migration-evidence)：過去の提出・移行の根拠資料。

## ライセンス

自作の設定への寄与、スクリプト、文書には [MIT License](LICENSE) を適用します。第三者の MOD、Shader、ライブラリ、生成された設定本文やコメントの権利は各作者に帰属します。適用範囲と配布物内の通知は [THIRD-PARTY-NOTICES.txt](pack/overrides/THIRD-PARTY-NOTICES.txt)を参照してください。
