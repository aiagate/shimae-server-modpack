# 0.0.6-local.3：ChunkyとCreate: Stats & Powerの両側除去候補

未公開のMinecraft 1.21.1 / NeoForge 21.1.266候補です。base HEAD `d4cbaeb903e805be8e794d74767f1d86997c287b`、branch `update/neoforge-mods-local`。前候補local.2の未コミット変更は `/home/hermes/workspace/mc-modpack-update/source-local.2-preserved` に保全しています。証跡・配布ZIP・再現手順は `/home/hermes/outputs/mc-modpack-update/without-chunky/` に置き、過去成果物は上書きしていません。

| 除去対象 | project / file | 実JAR内のmod ID | 正確なJAR名 |
| --- | --- | --- | --- |
| Chunky 1.4.23 | 485681 / 6383261 | chunky | Chunky-NeoForge-1.4.23.jar |
| Create: Stats & Power 1.16.0 | 1511282 / 9287207 | create_stats | create_stats-1.16.0.jar |

実refs、保存済み配布metadata、SHA-1検証済みJAR内の正式displayName/modIdを照合しました。両側の参照から対象2件だけを除き、client 200 / server 189件としました。VSS（1591852 / 8753475）は引き続き不在です。Create本体・他アドオン・DH 3.3.3・C2ME 0.4.0-alpha.0.124・Sable 2.0.6、その他全project/file IDはlocal.2と同じです。従来の49更新は、今回除去したCreate Statsの1件を除く48更新を維持します。Cool Rainのclient専用化、Cristel Libの不足キー補完、Thirst Was Reclaimedへの置換も維持します。

設定は `config/chunky/config.json`、`create_stats-client.toml`、`create_stats-common.toml` を削除しました。共有設定では `submarine_hull.json` のcreate_stats船体33項目、Sound Physicsの対象sound rate 4行、Apotheosisの空のpilot helmet名前生成1グループだけを除き、他MODの項目を保持します。DH入力設定は変更していません。過去版のmigration.jsonや履歴にある対象MOD情報は、歴史的記録として保持します。

client/server別の再帰MOD依存・必須依存・導入済み任意依存・非互換をMaven version rangeで検査し、除去対象への必須依存はありません。前候補と同じMinecraft宣言範囲警告9件だけが残ります。Jar-in-Jarはclient 104 / server 98 groupすべて充足しました。既存81テスト、compile、diff check、固定Go 1.27.2 / packwizによるbuild、独立rebuildの内容比較、publication dry-runが成功しました。

最終候補の新規worldでDone→save-all flush→正常停止、同じworldで再起動Done→save-all flush→正常停止を実行しました。両回とも終了コード0・強制停止なし、189個の実JARを最終server refsとhashで照合し、起動Mod ListでDH/Create/Sable存在、Chunky/create_stats/VSS不在を確認しました。seed 176321とworld名を維持し、world timeは391→796へ進みました。環境はJava Temurin 21.0.13+9、`-Xms512M -Xmx3G`、`127.0.0.1:25595`、online-mode有効、RCON/query無効、使い捨てworldです。

local.2の初回と初回・再起動と再起動を比較すると、`Chunky is not loaded.` は各3回→0回となり、関連するEventBus例外とC2ME chunk load event ERRORも消えました。同時に2MODを除去した最終候補の比較結果であり、単独要因の切り分け実験ではありません。新しいERROR種別はなく、recipe 22 / loot 546のエラーID集合は同じです。invalid dist 2クラス、Sableのcopycat_catwalk/linearbearing物理定義、tracksタグ、createqol superheated_lavaの既存エラーは残ります。構造物設定の不足エラーは0です。

MODによる起動時の設定書換えは配布入力と区別し、`config-runtime-review.json` と差分に保存します。DHのschema 4→5への自動移行（距離128→256、thread 12→3、帯域5000→500等）は前候補と共通です。生成serverId以外の実効DH値が前候補と同じであることを照合しました。配布設定は生成済み設定で上書きしません。

導入はREADMEとserver ZIP内README-SERVER.mdに従います。新しいCurseForge Appプロファイル・サーバー用空ディレクトリを推奨します。上書きの場合は停止・バックアップ後、両側の実際のmodsから次の残留JARを退避または削除します。

- `Chunky-NeoForge-1.4.23.jar`
- `create_stats-1.16.0.jar`（旧環境では `create_stats-1.15.0.jar` も）
- `vss-0.2.12-neoforge-1.21.1.jar`

Create本体と他アドオン、DH設定、world、キャッシュを残し、client/server双方のloaderをmanifestのNeoForge 21.1.266へ揃えます。以前共有されたNASの `NEOFORGE_LOADER_VERSION=21.1.243` は異なるため現地で実効値を確認してください。本作業でNAS接続・Compose・ルーター・既存world/cacheの変更は行いません。

Create Statsの実JARには188個のblockstate JSON、273個のitem model JSON、`TableAlarmCalendarSavedData` と `FreightManifestSavedData` クラスが含まれます。これは実登録数の断定ではなく資源/クラスの件数です。`create_stats:stats_display_panel`、`kinetic_flywheel`、`power_connector`、`pilot_helmet` 等のブロック・アイテムを使う既存worldでは提供元が失われ、読み込み・保存によって欠落コンテンツが失われる可能性があります。専用データも機能しなくなるため、停止したworldのバックアップを隔離コピーで試験し、原本のworldやデータを削除しないでください。根拠は `create-stats-content-impact.json`、`removed-create_stats-resources.json` とJAR由来mod定義に保存します。Chunkyは事前生成機能で、削除によりChunkyの操作/タスク再開は使えなくなります。既に生成された通常のチャンクを削除する操作はありません。

以前の既存world実プレイ移行試験はユーザーから「Done」と申告されています。当方が実行・検証した結果ではなく、今回の最終local.3における既存world移行成功とは扱いません。最終候補のクライアントGUI・ログイン・実プレイ、craft/drop、Jade表示、ドッキング、長時間負荷、本番timeout改善は未検証です。配布はmanifestインストーラー入力ZIPで、JAR/Java/world/秘密情報/EULA同意を含みません。exporterの `runtime_verified:false` を保持し、別runtime-validation.jsonへ実起動結果を記録します。commit/push/PR/releaseは行っていません。
