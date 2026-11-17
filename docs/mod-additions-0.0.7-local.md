# 0.0.7-local.3 追加候補

正式0.0.6（05fc330ea4f4a8f72f1ed543c443b31b19d31624）からのローカル試案です。公開版ではありません。

| MOD | 版 | project / file | 適用先 |
|---|---|---|---|
| Aeronautics: simulated copycats | 1.3.2 | 1558561 / 8727434 | client/server |
| Create: Loconautics | 0.1.3BETA | 1793084 / 9627028 | client/server |
| Create: Coasters Simulated | 0.1.6 | 1601871 / 9654233 | client/server |
| Let it Walk! | 0.1.5 Beta | 1780503 / 9540966 | client/server |
| Contraption Lights | 1.6.0 | 1599108 / 9546377 | clientのみ |
| LambDynamicLights | 4.8.11+1.21.1 | 393442 / 8780227 | clientのみ |

local.2へ最後の2件をclient専用で追加し、client 206 / server 193参照とします。LambのModrinth versionは `ksaGCvSu` です。NeoForge runtime、SpruceUI、Yumi等はJAR内包で、追加の外部依存は不要です。既存Create Coasters 2.0（1298151 / 8110328、mod ID createcoasters）は別MODとして維持します。

MC 1.21.1 / NeoForge 21.1.266 / Create 6.0.10 / Aeronautics・Simulated 1.3.2 / Sable 2.0.6、Iris 1.8.14-beta.1、Sodium 0.8.13、内包Flywheel 1.0.6とVeil 4.3.2を維持します。DH設定と、IrisでComplementary Unbound r5.8.1を有効にする既存設定も維持します。サーバーの実参照はlocal.2と同一です。既存の配布形式どおりserver ZIPにはclient manifestが入り、Composeの除外IDでclient専用2件をサーバーへ導入しません。

追加設定は `config/contraptionlights-client.toml` の次の2行だけです。他の項目は1.6.0の既定値で読み込ませます。

```toml
[general]
mode = "LAMB"
```

LAMBはSable船→地形と地形→Sable船の通常光を扱う実装があります。Irisが存在するとVEIL方式は停止します。shaderpack使用中はContraption Lights由来の色光が停止します。通常Create contraptionへの逆方向照明はFlywheel backendが条件で、現shader構成での動作を約束しません。これは静的な機能確認であり、実描画の合格とは別です。

## 導入と利用者試験

1. client ZIPをCurseForge Appの新しい試験プロファイルへインポートし、MOD取得完了後に起動してください。ZIPはmanifest導入用で、MOD JAR・Java・world・EULA同意を同梱しません。
2. 既存プロファイルへ適用すると既存configが優先または保持される場合があります。ゲーム停止中に実際のプロファイルの `config/contraptionlights-client.toml` を開き、`[general] mode = "LAMB"` を確認してください。Sodiumの設定UIにあるContraption LightsのModeからも変更できます。配布ZIPに設定があることだけでは既存プロファイルの実効値は確定しません。
3. 別途追加した **Sodium Dynamic Lights / RyoamicLightsの本体JARとは併用不可**です。modeをOFFにするだけでは依存衝突を解消しません。本候補には両本体は入っていません。既存の `sodiumdynamiclights-client.toml` は残しますが、Lambの設定へ自動移行されません。手持ち・他entityの光源設定はLambのUIで別途確認してください。
4. 隔離したworldコピーで、Complementary Unbound r5.8.1の読込成功と実際のshader有効状態を確認し、夜の港で船の発光ブロック→岸、岸の固定松明→船の両方向を確認してください。船の傾斜・移動、船同士、閉鎖船室と開口、Copycats+発光材、再join後も分けて確認します。
5. 通常Create contraptionはSable船とは別に確認してください。地下のsky lightとAO、DH遠景LOD、複数船・灯数増加時の負荷も未保証です。色光比較は別試験としてshaderpackを使わない状態と `enableColoredLight=true` が必要です。今回の候補のshader設定は変更していません。

Coasters Simulatedの走行、Let it Walk!の歩行装置、既存world移行・性能も実プレイ確認が必要です。公開、NAS、既存Compose、本番worldは操作しません。

今回のZIPと検証範囲・実行結果・制約は `/home/hermes/outputs/mc-modpack-0.0.7-lamb/REPORT.md`、`client-validation.json`、`checks.json` を参照してください。local.2の専用サーバー新規world起動と再起動の証拠は `/home/hermes/outputs/mc-modpack-0.0.7-expanded/runtime-validation.json` に保全されています。今回はclientのみの追加なので、その証拠を今回のclient GUIや照明描画の検証結果とは扱いません。
