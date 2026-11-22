# Changelog

## 0.1.0

- クライアント・サーバーともに、[Clutter No More 3.1.1](https://www.curseforge.com/minecraft/mc-mods/clutternomore/files/9397567) に戻し、3.1.3が Domum Ornamentum `1.0.231` を版指定で拒否する起動エラーに対処しました。
- 上書きする場合は両側の `mods` に `clutternomore-neoforge-3.1.3-1.21.1.jar` を残さないでください。3.1.2で追加されたDomum Ornamentum向けの連携修正は含みません（[瓦の形状変更に関する既知の問題](https://github.com/Monad-Modding/ClutterNoMore/issues/83)）。

## 0.0.9

- クライアント・サーバー両方から Thirst Was Reclaimed 3.0.7（884742 / 9593285）を削除。専用設定、JEIの表示順の項目、Sand Filterの船体設定も収録しません。
- 上書き導入時は、停止・ワールドのバックアップ後に両側の `mods` から `ThirstWasReclaimed-1.21.1-3.0.7.jar` を退避してください。Sand Filterなど同MODのブロック・アイテムは移行時に失われる可能性があります。

## 0.0.8

- Create: Tracks 1.0.1（1519765 / 7968280）を Create: Tracks+ 1.0.6b7（1548863 / 9185485）へ両側で置換。mod IDは同一の `tracks` で、既存 `config/tracks-server.toml` をそのまま使用します。上書き導入時は旧JAR `tracks-neoforge-1.21.1-1.0.1.jar` を両側から退避してください。
- Items Displayed 2.0.10、Create: Ornithopter Glider 1.2.1、Better Days 3.3.6.3、Streams Reflowing 2.17.5、Clutter No More 3.1.3をclient/server両側へ追加。
- New Year's Delight 2.0.2は既存参照のまま、`newyearsdelight-common.toml` で newYear mode を OFF に固定。季節コンテンツは自動では発生しません。
- Better Days は `betterdays-common.toml`（WhiteNoise設定）で昼25分・夜15分（20TPS・睡眠なし換算）を指定。睡眠の挙動は既定のまま変更しません。

## 0.0.7

- Simulated Copycats 1.3.2、Loconautics 0.1.3BETA、Coasters Simulated 0.1.6、Let it Walk! 0.1.5 Betaを追加。既存Create Coasters 2.0は維持。
- client専用でContraption Lights 1.6.0とLambDynamicLights 4.8.11+1.21.1を追加。LAMB方式を指定し、Iris・shader・DH設定を保持。shaderpack使用中の色光には制約があります。

## 0.0.6

- NeoForge を 21.1.266 へ更新（Minecraft 1.21.1 維持）。
- 0.0.5からMOD 48件を更新し、Cool Rainをクライアント専用へ修正。Cristel Libの構造物設定を補完し、既存の生成頻度を維持します。
- Chunky、Create: Stats & Power、VSSを両側から除去。Create本体・他アドオン・Distant Horizons設定を維持します。
- 上書き導入では廃止JARを両側から退避し、全員のloaderを21.1.266へ揃えてください。Create Stats由来の既存コンテンツは提供元を失うため、worldのバックアップが必要です。

## 0.0.5

- Thirst Was Taken 2.1.5 を Thirst Was Reclaimed 3.0.6 に置換し、Jade 15.10.6 の流体表示時に発生する既知の Mixin 競合を除去。
- Thirst の設定を後継版に合わせて調整。クライアント・サーバーとも 0.0.5 に更新し、旧 Thirst と併用しないでください。

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
- 各 MOD の固定参照と設定を同梱。
- Apotheosis / Enchanting の連携設定を追加。
