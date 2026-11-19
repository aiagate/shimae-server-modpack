# 0.0.8 追加MOD・置換と検証範囲

正式0.0.7（git commit `4ffaf1af8f80f336c7e356b88defce6ace3b3e0b`、Minecraft 1.21.1 / NeoForge 21.1.266、client 206 / server 193参照）を基点に、Create: Tracks を Tracks+ へ置換し、5件を両側へ追加します。client 211 / server 198参照。既存のDH・Iris・LAMB・Create各設定は変更しません。

## 参照の変更

| MOD | 版 | project / file | 適用先 | 備考 |
|---|---|---|---|---|
| Create: Tracks → Create: Tracks+ | 1.0.1 → 1.0.6b7 (beta) | 1519765 / 7968280 → 1548863 / 9185485 | client/server | 置換。mod IDは同一 `tracks` |
| Items Displayed | 2.0.10 | 937042 / 7234377 | client/server | 依存なし |
| Create: Ornithopter Glider | 1.2.1 | 1312780 / 9258973 | client/server | Create必須・Curios任意、パック保有で充足 |
| Better Days | 3.3.6.3 | 895618 / 7978626 | client/server | WhiteNoise内包 |
| Streams Reflowing | 2.17.5 | 1581408 / 9639263 | client/server | 依存なし |
| Clutter No More | 3.1.3 | 1339454 / 9491575 | client/server | 依存すべて任意（JEI統合可） |
| New Year's Delight | 2.0.2（既存） | 1451118 / 9551236 | client/server | 参照不変、設定を追加 |

上書き導入時は、両側の実modsフォルダから旧JAR `tracks-neoforge-1.21.1-1.0.1.jar` を停止後に退避してください。新JARは `tracks_plus-1.0.6b7.jar` です。同一mod IDのため旧JARが残ると二重読込になります。

## 実JARの同一性検証（2026-11-19取得）

追加5件で、CurseForge配布ファイルとModrinth配布ファイルのSHA256が一致しました。Clutter No More は配布元によってファイル名が異なりますが、バイト列は同一です。Tracks+とNew Year's DelightはCurseForgeの固定ファイルのSHA256を記載します。

| MOD | SHA256 |
|---|---|
| Items Displayed 2.0.10 | `a0a691e050778fc18120f8ba87d8ac9619db84ad229ff3ebafe53a0da6f28a4a` |
| Create: Ornithopter Glider 1.2.1 | `de84f20bc680dbb7bbc18460cf87bd67382c80f74434fac61699070872f3860f` |
| Better Days 3.3.6.3 | `03acad0637dd5d86361178eb3e87ad8f2ed965e9c84514df4dc4228bb24aa2aa` |
| Streams Reflowing 2.17.5 | `bac3ca024434359d70ce920cddb6b374616a49ff1134da0717110ad0152422c4` |
| Clutter No More 3.1.3 | `012146b004b8b44b8c5152b476bdae6ac266677a65092610db0f2d49ca8e04f2` |
| New Year's Delight 2.0.2 | `75976acbb1ac4a60184d0af5804029ca836c191e5cf93fc5a0fac4609d1a804a` |
| Create: Tracks+ 1.0.6b7 | `97a4891caf7defc84a0e57e88d3db829ddee4c1966b22ba2e9a02ae548503627`（CF pinの実JAR） |

追加・置換分はすべてCurseForgeの固定参照で配布します。JARはZIPに同梱しません。

## 設定の追加

### New Year's Delight 2.0.2 — `config/newyearsdelight-common.toml`

実JAR（`com/newyearsdelight/Config.class`）の `newYear.mode` は enum `NewYearMode`（`LUNAR` / `REAL_CALENDAR` / `OFF`）です。NeoForgeのCOMMON設定で、mod ID `newyearsdelight` の既定ファイル名 `newyearsdelight-common.toml` へ出力されます。本packは次の通り新規追加します。

```toml
[newYear]
mode = "OFF"
```

`OFF` は季節イベントの自動発生を無効にする設定です。MOD自体は削除しません。**起動後にOFFが保持されるか**は実機未確認です。

### Better Days 3.3.6.3 — `config/betterdays-common.toml`

WhiteNoise 2.2.0をJAR内包し、設定ファイル名はWhiteNoiseの `%s-%s.toml`（mod ID + 種別小文字）規約で `betterdays-common.toml` です。`[time]` の実在キー `speedMethod` / `dayStart` / `nightStart` / `daySpeed` / `nightSpeed` / `enableInterpolatedTime` を使い、昼25分・夜15分（20TPS・睡眠なし換算）を指定します。

- 昼区間 23500→12500（13000tick）を30000実tickで進める `daySpeed = 13000/30000 = 0.43333333333333335`
- 夜区間 12500→23500（11000tick）を18000実tickで進める `nightSpeed = 11000/18000 = 0.6111111111111112`

日の出・日の入り境界はMOD既定値を保持します。睡眠の挙動は既定のまま変更しません。記載していないキー（`daySpeedMinutes` / `nightSpeedMinutes` / 補間・effects系）はMOD既定で読み込まれ、WhiteNoiseが不完全なファイルを自動補正します。**実効反映（20TPS実サーバーでの昼・夜の実長）** は実機確認の残課題です。

### Create: Tracks+ — 既存 `config/tracks-server.toml` 維持

旧Create: Tracks 1.0.1とTracks+ 1.0.6b7は同一パッケージ `dev.qwxon.tracks` のSERVER設定で、ファイル名も同一の `tracks-server.toml` です。既存override（`[server] enableRenderTuningCheats = false`）はそのまま有効で、Tracks+が追加する `enableTerrainDebugVisualization` は実行時に既定値 false で補完されます。

## 個別の注意

- **Streams Reflowing**: 確認する場合は新規チャンクを使ってください。既存の地形生成MODとの互換性は実機未確認です。
- **Clutter No More**: 階段やハーフブロックのクラフト・建築手順が変わります。構造物MODが出力する階段・スラブとの相互作用は未検証です。
- **Create: Ornithopter Glider**: Create 6.0.10・Curios APIはパック保有のため依存は充足しています。Create 6.0.x + Aeronautics大量導入環境でのMixin実動作は未検証です。
- **Items Displayed**: 依存なし。陳列用の表示装置を追加します。

## 任意候補（正式収録なし）

**Ji AFK Cinematic 2.4.0-beta.1.1**（Modrinth `ji-afk-cinematic` version `r16Oum5Z`、CurseForge project 1697412）— AFK Cinematics本体がFabric専用のための代替候補です。ModrinthではNeoForge 1.21.1向けビルドが存在しますがbetaのみで、CurseForge側にはNeoForgeタグ付きファイルがありません（cfwidget照合：NeoForgeタグ0件）。正常動作が未確認のため、**本リリースには収録していません**。収録する場合は実機での起動・動作確認（依存含む）を先に行い、CF側に同JARが提出された場合のみ通常参照へ昇格させてください。権利や審査の状態を無視した同梱は行いません。

**Compact Controls** — 旧候補の不採用（レシピ不成立）を維持します。

## Thirst Was Reclaimed（維持・手順のみ追記）

Thirst Was Reclaimed 3.0.7（884742 / 9593285）は参照・既存設定とも変更しません。MODはプレイヤー単位の ON/OFF コマンドを持つため、喉の渇きを無効にしたい場合は運用者が次を実行できます。

```
/thirst enable @a false
```

これは導入手順（[サーバー導入手順](server-setup.md)）への記載のみで、**本番NAS・Compose・既存worldでは未実行**です。MODの削除・常時の挙動変更は行いません。

## 検証範囲と残課題

実施済み（本候補構築時点）:

- 追加・置換6件の固定参照、設定ファイル名・キー、client/server ZIPの内容を確認。
- ビルドと配布の確認手順は [開発・ビルド手順](development.md) と [公開手順](publishing.md) を参照。

未実施（実機確認を要するため、別途実施）:

- 0.0.8の実サーバー動作とStreams Reflowingの地形生成互換性
- Clutter No More等コンテンツMODの実レシピ確認
- Better Days の実効時間反映、New Year's Delight のOFF保持
- client GUI・FPS・本番world移行
