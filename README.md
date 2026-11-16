# Shimae Server Modpack

Minecraft 1.21.1 向けの Modpack です。クライアント用の CurseForge manifest ZIP と、Docker で導入する Server Pack を配布します。

正式版 `0.0.6` は検証済み `0.0.6-local.3` の構成を引き継ぎ、全員Distant Horizons（DH）で遠景描画を行う構成です。直前候補 `0.0.6-local.2` からChunky（project 485681 / file 6383261）とCreate: Stats & Power（project 1511282 / file 9287207、mod ID `create_stats`）をclient/server両方から除き、client 200 / server 189参照としました。VSS除去は継続します。Create本体と他アドオン、Minecraft 1.21.1 / NeoForge 21.1.266、DH 3.3.3、C2ME 0.4.0-alpha.0.124、Sable 2.0.6、DH設定は維持します。以前の49更新から、今回削除したCreate Statsの更新分を除く48更新を引き継ぎます。[候補段階の検証記録](docs/mod-update-0.0.6-local.md)を確認してください。

0.0.6のクライアントZIPはCurseForge Appの新しいプロファイルへインポートし、サーバーZIPは[導入手順](docs/server-setup.md)どおり別の空ディレクトリへ展開します。上書き導入では廃止JARが残るため、停止・バックアップ後に**両側の実際の `mods` から `Chunky-NeoForge-1.4.23.jar`、`create_stats-1.16.0.jar`（旧環境では `create_stats-1.15.0.jar` も）、`vss-0.2.12-neoforge-1.21.1.jar` をmods外へ退避または削除**してください。Create本体と他アドオンは残します。削除MOD専用の `config/chunky/`、`create_stats-client.toml`、`create_stats-common.toml`、VSS設定2ファイルは退避できます。**DH設定・world・キャッシュは維持**し、同じ0.0.6とloaderへ全員を揃えます。

Create StatsのJARには `create_stats` 名前空間の表示パネル・電気機械・扉・ヘルメット等のblock/item資源、レシピが実在します。これらを含む既存worldでは提供元が失われ、読み込み・保存で欠落コンテンツが失われる可能性があります。worldをバックアップして隔離コピーで確認してください。今回の試験は新規worldです。以前の既存world実プレイ移行試験はユーザーからDoneと申告されていますが、この構成に対する当方の検証済み結果ではありません。

既存NAS Composeについて共有された `NEOFORGE_LOADER_VERSION=21.1.243` は、0.0.6のmanifestの `neoforge-21.1.266` と異なります。本番Composeの現在値と実効loaderを現地で読み戻し、移行前に一致させる必要があります。この作業ではNASへ接続せず、既存Composeも変更していません。クライアント実プレイ、本番既存worldの移行とtimeout改善は未検証です。

## ダウンロードと導入

正式0.0.6の配布先は [GitHub Release](https://github.com/aiagate/shimae-server-modpack/releases/tag/v0.0.6) と [CurseForge](https://www.curseforge.com/minecraft/modpacks/shimae-server-modpack/files)（project ID `1733082`）です。CurseForgeの審査状況・受付IDはActionsの公開検証receiptで確認できます。

クライアントには `shimae-server-modpack-0.0.6.zip` を使用します。CurseForge App で ZIP をインポートし、MOD の取得後に起動してください。サーバーには同じ版のクライアントで接続します。

サーバーには `shimae-server-modpack-0.0.6-serverpack.zip` を使用します。この ZIP は導入用で、MOD JAR や Java を同梱した起動可能なサーバー一式ではありません。[サーバー導入手順](docs/server-setup.md)と ZIP 内の `README-SERVER.md` を参照してください。

## 配布内容

| 項目 | 0.0.6 の内容 |
| --- | --- |
| Minecraft / loader | 1.21.1 / NeoForge 21.1.266 |
| クライアント | 固定参照 200 件、設定、ライセンス文書 |
| サーバー | サーバー用参照 189 件、設定、ライセンス文書、Compose と導入手順 |

配布 ZIP に MOD JAR、world、接続先、認証情報は含めません。サーバーの manifest はクライアントと同一で、Compose がクライアント専用の 11 project ID を除外します。

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
