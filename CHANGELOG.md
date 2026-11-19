# Changelog

## 0.0.9

- クライアント・サーバー両方から Thirst Was Reclaimed 3.0.7（884742 / 9593285）を削除。専用設定、JEIの表示順の項目、Sand Filterの船体設定も収録しません。他のMODの固定参照は0.0.8と同じです（client 210 / server 197）。
- 上書き導入時は、停止・ワールドのバックアップ後に両側の `mods` から `ThirstWasReclaimed-1.21.1-3.0.7.jar` を退避してください。Sand Filterなど同MODのブロック・アイテムは移行時に失われる可能性があります。実機テスト・既存ワールドの移行は未実施です。

## 0.0.8

- 正式0.0.7（4ffaf1af8f80f336c7e356b88defce6ace3b3e0b）基点。Minecraft 1.21.1 / NeoForge 21.1.266、client 211 / server 198参照。
- Create: Tracks 1.0.1（1519765 / 7968280）を Create: Tracks+ 1.0.6b7（1548863 / 9185485）へ両側で置換。mod IDは同一の `tracks` で、既存 `config/tracks-server.toml` をそのまま使用します。上書き導入時は旧JAR `tracks-neoforge-1.21.1-1.0.1.jar` を両側から退避してください。
- Items Displayed 2.0.10、Create: Ornithopter Glider 1.2.1、Better Days 3.3.6.3、Streams Reflowing 2.17.5、Clutter No More 3.1.3をclient/server両側へ追加。追加5件はCurseForgeとModrinthの実JARのSHA256が一致し、Tracks+はCurseForgeの固定ファイルを確認しました。
- New Year's Delight 2.0.2は既存参照のまま、`newyearsdelight-common.toml` で newYear mode を OFF に固定。季節コンテンツは自動では発生しません。OFFが起動後生成設定で保持されるかは確認対象です。
- Better Days は `betterdays-common.toml`（WhiteNoise設定）で昼25分・夜15分（20TPS・睡眠なし換算）を指定。睡眠の挙動は既定のまま変更しません。
- Thirst Was Reclaimed は参照・設定とも維持。`/thirst enable @a false` によるプレイヤー単位の無効化を導入手順にのみ記載しました。本番では未実行で、常時の挙動は変更しません。
- AFK Cinematics（Fabric専用）は不採用。代替のJi AFK CinematicはNeoForge 1.21.1向けの該当ファイルがCurseForgeにないため不収録。
- Compact Controlsの旧不採用（レシピ不成立）を維持。
- 6件の実機同居テスト・レシピ確認・client GUI・本番world移行は未検証。[追加MODと検証範囲](docs/mod-additions-0.0.8.md)を参照してください。

## 0.0.7

- 0.0.7-local.3を正式版へ昇格。Minecraft 1.21.1 / NeoForge 21.1.266、client 206 / server 193参照。
- Simulated Copycats 1.3.2、Loconautics 0.1.3BETA、Coasters Simulated 0.1.6、Let it Walk! 0.1.5 Betaを追加。既存Create Coasters 2.0は維持。
- client専用でContraption Lights 1.6.0とLambDynamicLights 4.8.11+1.21.1を追加。LAMB方式を指定し、Iris・shader・DH設定を保持。shaderpack使用中の色光には制約があります。
- 一部追加MODはBeta版です。専用サーバー新規world起動・保存・再起動を確認。client GUI・照明描画・FPS・装置実動作・本番world移行は未検証。[固定参照と導入上の注意](docs/mod-additions-0.0.7.md)を参照してください。

## 0.0.6

- 検証済み0.0.6-local.3を正式版へ昇格。Minecraft 1.21.1 / NeoForge 21.1.266、client 200 / server 189の固定参照を使用します。
- 0.0.5からMOD 48件を更新し、Cool Rainをクライアント専用へ修正。Cristel Libの構造物設定を補完し、既存の生成頻度を維持します。
- Chunky、Create: Stats & Power、VSSを両側から除去。Create本体・他アドオン・Distant Horizons設定を維持します。
- 上書き導入では廃止JARを両側から退避し、全員のloaderを21.1.266へ揃えてください。Create Stats由来の既存コンテンツは提供元を失うため、worldのバックアップが必要です。
- 新規worldの起動・保存・再起動済み。クライアント実プレイ、本番既存world移行とtimeout改善は未検証です。[候補段階の検証履歴](docs/mod-update-0.0.6-local.md)を参照してください。

## 0.0.6-local.3 (unpublished candidate)

- Chunky 1.4.23（485681 / 6383261）とCreate: Stats & Power 1.16.0（1511282 / 9287207、create_stats）をclient/server両側から除去。client 200 / server 189参照。
- 両MOD専用設定3ファイルと、共有設定内のcreate_stats専用の船体33項目・音4項目・空の名前生成1グループのみ除去。
- VSS除去、Create本体・他アドオン・DH設定・Minecraft/loaderを維持。従来49更新から削除対象Create Statsの1件を除く48更新を継承。
- 残留JARの正確な除去名、Create Statsの既存ブロック・アイテム喪失リスク、DH設定維持、loader一致を導入手順へ記載。
- 最終候補の実サーバー起動・保存・同world再起動、依存、既存テスト、ZIP再現性の結果は[検証記録](docs/mod-update-0.0.6-local.md)と独立runtime receiptへ保存。以前の既存world移行試験Doneはユーザー申告として記録し、当方の最終候補検証と区別。

## 0.0.6-local.2 (unpublished candidate)

- 全員DHで遠景描画を行うため、VSS project 1591852 / file 8753475をclient/server両参照から除外。専用設定2ファイルも除去し、client 202 / server 191参照。
- local.1のMinecraft、NeoForge、DH、C2ME、Sable 2.0.6、他49更新と既存設定を固定。Chunkyは保持し、既知例外は残課題として継続。
- 上書き導入で残ったVSS JARの両側からの退避手順と、NAS loader設定の読み戻しが必要な点をREADMEへ記載。
- ローカル専用サーバーの実行結果は新候補用の独立した検証記録へ保存。クライアント実プレイ・本番timeout改善は未検証。

## 0.0.6-local.1 (unpublished candidate)

- Minecraft 1.21.1を維持し、NeoForgeを21.1.266へ更新。21.1.262で修正された既知DoS問題3件に対応。
- MOD 49件（サーバー共通47件）を更新。固定参照・依存・配布ハッシュを全203件確認。
- 専用サーバーで致命的エラーを再現したCool Rainをクライアント専用に修正（client 203 / server 192参照）。
- Cristel Libの構造物設定の不足キーを補完し、既存の生成頻度などの調整値を保持。
- ローカル専用サーバーで新規ワールドの起動・保存・再起動を検証。既存の非致命的なレシピ／互換エラーは残るため、実プレイ・既存ワールド移行の検証は別途必要。[検証記録](docs/mod-update-0.0.6-local.md)参照。

## 0.0.5

- Thirst Was Taken 2.1.5 を Thirst Was Reclaimed 3.0.6 に置換し、Jade 15.10.6 の流体表示時に発生する既知の Mixin 競合を除去。
- Thirst の設定を後継版に合わせて調整。クライアント・サーバーとも 0.0.5 に更新し、旧 Thirst と併用しないでください。
- Aero のドッキングコネクタ設置・注視の実機再現試験は未実施です。[検証記録](docs/thirst-fix-0.0.5.md)を参照してください。

## 0.0.4

- Create: Design n' Decor 2.2b と Create Coasters 2.0 を追加。
- Coasters の Booster / Speed Limiter / Seat Locker にサバイバル用クラフトレシピを追加。
- OpenLoader 21.1.5 と Prickle 21.1.11 を追加し、レシピデータパックを全ワールドへ自動適用。
- JEI で通常のCreativeタブに載らないアイテムも検索対象に追加。

## 0.0.3

- クライアントの MOD 88 件（サーバー共通 84 件）を更新。
- Aeronautics と同梱コンポーネント、依存ライブラリを更新。
- Quark と Supplementaries を更新。

## 0.0.2

- クライアント用の CurseForge manifest ZIP とサーバー用の Server Pack を配布。
- Docker / AUTO_CURSEFORGE によるサーバー導入に対応。

## 0.0.1

- Minecraft 1.21.1 / NeoForge 21.1.243 向けの初版を追加。
- 199 件の MOD に対応し、各 MOD の設定を同梱。
- Apotheosis / Enchanting の連携設定を追加。
