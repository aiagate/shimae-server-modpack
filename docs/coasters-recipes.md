# Coasters のサバイバル用レシピ

ModPack 0.0.4 / Minecraft 1.21.1 / NeoForge 21.1.243 用。作業台またはインベントリのクラフト欄で、素材を順不同に並べます。いずれも完成品は1個です。

| 完成品 | 素材 |
| --- | --- |
| Booster | 安山岩ケーシング ×1、精密機構 ×1、レッドストーンダスト ×1 |
| Speed Limiter | 安山岩ケーシング ×1、回転速度コントローラー ×1 |
| Seat Locker | 真鍮ケーシング ×1、鉄インゴット ×1、レッドストーンダスト ×1 |

## 配布と更新

データパックの正本は `pack/overrides/config/openloader/packs/shimae_coasters/`。Minecraft 1.21.1 のデータパック形式48、単数形の `recipe` ディレクトリと `result.id` を使用します。レシピIDは `shimae:coasters/boost_block`、`shimae:coasters/speed_block`、`shimae:coasters/lock_block` です。

OpenLoader が `config/openloader/packs/` のフォルダ形式データパックを読み込み、ゲームインスタンス内の全ワールドに適用します。通常の client export と Server Pack の設定抽出に含まれるため、world を配布したり、各ワールドの datapacks フォルダへ手動コピーしたりする必要はありません。既存環境は更新したパックのMOD参照とconfigを反映して再起動してください。

| 追加MOD | project ID | file ID | 必須依存 |
| --- | --- | --- | --- |
| OpenLoader 21.1.5 | 354339 | 6546293 | Prickle >=21.1、<21.2、NeoForge >=21.1.133、Minecraft >=1.21.1、<1.22 |
| Prickle 21.1.11 | 1023259 | 6961457 | NeoForge >=21.1.61、Minecraft >=1.21.1、<1.22 |

配布先は[OpenLoader公式](https://www.curseforge.com/minecraft/mc-mods/open-loader)、[Prickle公式](https://www.curseforge.com/minecraft/mc-mods/prickle)。JARはリポジトリや配布ZIPに同梱せず、manifestの固定参照から取得します。自作レシピはリポジトリのMITライセンスに従います。

## JEI検索への表示

`config/jei/jei-client.ini` の `showHiddenIngredients = true` を配布設定に反映しています。通常のCreativeタブから収集されないアイテムもJEIの一覧へ追加する設定で、他MODの隠れたアイテムも対象です。MOD ID検索は有効なので、検索欄に `@createcoasters` と入力できます。既存インスタンスへ更新する場合は、この設定ファイルの反映も確認してください。
