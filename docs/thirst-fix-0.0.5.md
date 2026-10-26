# 0.0.5: Thirst / Jade の Mixin 競合対策

## 変更対象

Minecraft 1.21.1 / NeoForge 21.1.243 のまま、client / server の固定参照を次の一組だけ置換します。packwiz 用メタデータはビルド時生成で、別の依存ロックはありません。

| MOD | CurseForge project / file | 配布 JAR |
| --- | --- | --- |
| 削除: Thirst Was Taken 2.1.5 | 679270 / 7017923 | ThirstWasTaken-1.21.1-2.1.5.jar |
| 追加: Thirst Was Reclaimed 3.0.6 | 884742 / 8893710 | ThirstWasReclaimed-1.21.1-3.0.6.jar |

Aero 1.3.2、Sable 2.0.6、Create 6.0.10、Jade 15.10.6 を含む他の固定参照は変更しません。client 203 / server 193 件は変わりません。旧 Thirst と後継版は同じ `thirst` ID を使用するため併用できません。クライアント・サーバーを同じパック版に揃えてください。

## 原因と一次情報

報告された例外は `thirst.mixins.json:jade.MixinFluidView` の injection check failure で、Jade の `JadeForgeUtils.fromFluidHandler` → `FluidStorageProvider` から発生しています。Aero のコネクタが流体情報を参照させる契機になった可能性がありますが、コネクタ自体の不具合と確認したものではありません。

- [Taken の同一バージョン・同一例外の報告](https://github.com/ghen-git/Thirst-Mod/issues/280)
- [後継版の Jade 連携変更と Mixin 削除](https://github.com/mlus-asuka/Thirst-Was-Reclaimed/commit/83ab7ec2c704e949b2b9bfba6d12db229afdb6d8)
- [Reclaimed 3.0.6 の MC 1.21.1 / NeoForge 配布ファイル](https://www.curseforge.com/minecraft/mc-mods/thirst-was-reclaimed/files/8893710)
- [3.0.6 のソース](https://github.com/mlus-asuka/Thirst-Was-Reclaimed/tree/48f5436)

公式 CDN から取得した Reclaimed JAR の SHA-256 は `26e3bf4ccf1f0d881609ac3f972f20aed4c9dd90090cd290f9ebf611b4db4503`。実 JAR の Mixin 一覧に `jade.MixinFluidView` がないことを確認しました。JAR の必須条件は NeoForge `[21.1.128,)`、Minecraft `[1.21,1.21.3)` で、パックの版を満たします。

## 設定と依存の確認

後継版も `config/thirst/` の同じ5ファイルを登録します。既存設定のキー・階層を 3.0.6 ソースと照合し、`common.toml` の廃止済み `defaultPurity` を削除、新設の `enablePurity = true` と `handDrinkingCooldown = 20` を公式デフォルト値で明記しました。手飲みの無効化、飲料・食品リスト、キーワード設定、表示位置などの既存値は維持します。既存インスタンスではローダーが古いキーを補正する可能性があるため、更新後の設定も確認してください。

2026-10-26 に、固定された203参照と置換候補を公式 CurseForge の公開ファイル情報・CDNから取得し、ID・ファイル名・サイズとZIP形式を照合しました。後継版を採用した201個の外側JAR（他2参照はShader ZIP）と同梱JAR、合計331 JARを調べました。

- NeoForge/Forge メタデータ上の必須MODはすべて外側または同梱JARに存在。全依存のバージョン範囲解決をローダーで試した結果ではありません。
- 他MODと同梱JARに `dev.ghen.thirst` / `dev/ghen/thirst` の直接参照はなく、`thirst` への宣言依存もなし。文字列・クラス定数の静的確認であり、動的な参照までは保証しません。
- Reclaimed の Jade への12種類のメソッド参照は、Jade 15.10.6 の実JAR内の宣言・継承先に存在。

## ビルドと検証範囲

- `python3 -m unittest discover -s tests -v`: 81テスト成功。
- `python3 -m compileall -q scripts tests`: 成功。
- 固定 Go 1.27.2 / packwiz `v0.0.0-20260218225342-dfd8b68a4796` で client / server ZIP を生成。Go アーカイブ SHA、packwiz のコンパイラー・module checksum を検証。
- 独立した2回のビルドで参照・設定内容一致を確認。既存 `publish_pair.py` の提出しない計画生成・検証を実行。
- 生成 manifest の旧project除去、新project一件、client/server整合性、設定配布、旧版から他MOD参照を変更していないことを確認。

専用サーバー起動、クライアント起動、ドッキングコネクタの設置・注視、飲水と流体純度の実機回帰試験は未実施です。検証環境から公式 NeoForge Maven ホストへの通信が HTTP 403 / CONNECT 拒否となり、ローダーを取得できませんでした。実ワールドや稼働サーバーには変更を加えていません。

この版は報告と一致する既知の Mixin 競合を除去する変更です。実環境でクラッシュが解消したと断定するものではありません。公開受付・審査・Server Pack 区分・CDN ハッシュの確認は、通常の公開手順で別途判定します。
