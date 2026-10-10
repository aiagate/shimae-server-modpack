# Release history and evidence

## 0.0.2 submission evidence


The published artifacts and receipts remain at their original locations.

- Client: CurseForge file 9104708, SHA256 `f9f14a87d8ed5589c5f619af35786147b0ecbfa56247346f5b2122f2f27b82c9`, 3,004,478 bytes.
- Server: CurseForge file 9104783, parent 9104708, SHA256 `49c213f137d56afabc245d6839706b0f181c034b90753e23e3b5616c5adf660a`, 3,018,116 bytes.
- [Initial Actions run](https://github.com/aiagate/shimae-server-modpack/actions/runs/37883897099) accepted the client; the child request returned HTTP400/error1013 without a file ID. The raw error message was not recorded.
- The author UI confirmed the client Approved/public and no additional server.
- [Reviewed one-time recovery](https://github.com/aiagate/shimae-server-modpack/actions/runs/37884989568) reused the exact saved ZIPs, omitted optional child gameVersionNames, and accepted server 9104783 without resending the client. The original claim, recovery claim and result remain immutable Release assets. Both parent approval and metadata changed, so the cause of error1013 is not established.
- The same accepted server's Additional File Info was changed from None to Server Pack in the author UI. No ZIP change or reupload occurred.
- [Publication verification](https://github.com/aiagate/shimae-server-modpack/actions/runs/37886221425) confirmed both Approved, parent linkage, Server Pack type and full CDN SHA256. Receipt artifact ID: 11596383556.
- [GitHub Release v0.0.2](https://github.com/aiagate/shimae-server-modpack/releases/tag/v0.0.2) retains both ZIPs and the immutable claim/result journal.

The completed version-specific recovery workflow/script was retired during
cleanup. Its exact implementation remains in Git at commit
`1217d7c05d48eec06124ad969707e9443fae36af`. Current partial-submission handling
is in publish_pair.py (server_only, existing parent verification, durable
claims/results, failure receipts). Unknown acceptance never authorizes a retry.

## 0.0.1 App migration evidence


Historical provenance, preparation and review records are consolidated here.
The complete original JSON records, including reference ordering, App-specific
fields and per-file hashes, remain in the [Git snapshot before consolidation](https://github.com/aiagate/shimae-server-modpack/tree/fe9d62b234f59b67f4febaa288b098105646734f/history/0.0.1-app).
These records formerly lived in `exports/` and the root `release.json`; recorded
paths describe that historical layout. Current build inputs are in `pack/`;
initial-migration checks use `pack/migration.json`. Published ZIPs, original user
exports and acceptance receipts remain in their existing Release/local locations.

Client199/server189 project/file ID maps match current `pack/client.refs.json`
and `pack/server.refs.json`. The client came from the user-supplied source
manifest; App execution and the profile UI were not independently observed.
Historical server references were desired-configuration comparison data from
local import candidates, not evidence of App export provenance or a prerequisite
for client publication. The full reference records remain in the Git snapshot.

### App source and release metadata

Historical `exports.lock.json`:

```json
{
  "schema_version": 1,
  "repository": "aiagate/shimae-server-modpack",
  "version": "0.0.1",
  "minecraft_version": "1.21.1",
  "mod_loader": "neoforge-21.1.243",
  "profiles": {
    "client": {
      "asset_id": 621353663,
      "filename": "shimae-server-modpack-0.0.1.zip",
      "sha256": "b27742177d000e581a6b9ea0bd1540929ac291018ab70ef11f9bd1193dacd81c",
      "size_bytes": 430127,
      "manifest_name": "Shimae Server Modpack",
      "reference_lock": "exports/client.refs.json",
      "origin": {
        "exporter": "CurseForge App",
        "confirmed": true,
        "confirmed_by": "User supplied this ZIP in response to the request for a client App Export; App execution was not independently observed.",
        "exported_at": "Export time not recorded; received 2026-10-08.",
        "source_profile": "Manifest name: Shimae Server Modpack; profile UI not independently observed.",
        "packaging": "cleaned-copy-with-unchanged-app-manifest",
        "original_sha256": "042de1c25ce9995f04eac015ba9e6db257749a677c5ad02f50293b5decac7cf8",
        "manifest_sha256": "91c40ad018a732ff58a984cddd3daf9209618ab53f4a69c04e35b2de616e7e12",
        "modlist_sha256": "68b73bda0d72d3d8ec770e5a4f2ec13378ed9815a6b5bee01e14843b606a3bf6"
      }
    }
  }
}
```

Historical `release.json`:

```json
{
  "project_id": 1733082,
  "export_asset_id": 621353663,
  "minecraft_version": "1.21.1",
  "loader_id": "neoforge-21.1.243",
  "game_version_names": [
    "1.21.1",
    "NeoForge",
    "Client"
  ],
  "release_type": "release",
  "display_name": "Shimae Server Modpack - 0.0.1",
  "reviewed_sha256": "b27742177d000e581a6b9ea0bd1540929ac291018ab70ef11f9bd1193dacd81c"
}
```

Historical `preparation.json`:

```json
{
  "schema_version": 1,
  "source_sha256": "042de1c25ce9995f04eac015ba9e6db257749a677c5ad02f50293b5decac7cf8",
  "manifest_sha256": "91c40ad018a732ff58a984cddd3daf9209618ab53f4a69c04e35b2de616e7e12",
  "modlist_sha256": "68b73bda0d72d3d8ec770e5a4f2ec13378ed9815a6b5bee01e14843b606a3bf6",
  "omit_paths": [
    "overrides/config/bonsaitrees4-client.toml",
    "overrides/config/bonsaitrees4-common.toml",
    "overrides/config/chunky/overworld.csv",
    "overrides/config/chunky/tasks/minecraft/overworld.properties",
    "overrides/config/gpushift/benchmarks/benchmark_2026-07-25_12-58-43.csv",
    "overrides/config/gpushift/benchmarks/benchmark_2026-07-25_12-58-43.txt",
    "overrides/config/minecolonies-client-1.toml.bak",
    "overrides/config/minecolonies-common-1.toml.bak",
    "overrides/config/minecolonies-server-1.toml.bak",
    "overrides/config/sodium-fingerprint.json",
    "overrides/config/witherreincarnated/client-1.toml.bak"
  ],
  "additions": {
    "overrides/LICENSE-Shimae.txt": "LICENSE",
    "overrides/THIRD-PARTY-NOTICES.txt": "LICENSE-SCOPE.txt"
  },
  "retained_config_policy": "All remaining current user file bytes retained, including changed/additional live settings."
}
```

### Reference and override review policy

```json
{
  "schema_version": 1,
  "basis": "Client: user-supplied 0.0.1 App-export input, reviewed packaging cleanup; source manifest/modlist and all retained settings unchanged. Server: prior local candidate comparison data only; not required for client publication.",
  "forbidden_project_ids": [
    302973,
    1546772,
    278993
  ],
  "retained_project_ids": [
    306770,
    283644,
    313970,
    898963,
    986583,
    1063926
  ],
  "client_only_project_ids": [
    60089,
    385587,
    394468,
    448233,
    455508,
    521480,
    678384,
    882495,
    1533254,
    1569619
  ],
  "expected_counts": {
    "client": 199,
    "server": 189
  },
  "commented_json_paths": [
    "overrides/config/lithostitched.json",
    "overrides/config/tectonic.json"
  ]
}
```

The historical override policy recorded 320 client file hashes and
308 server comparison hashes. Full hash maps remain in the Git snapshot;
current initial-migration hashes remain in `pack/migration.json`. All retained
settings, manifest and modlist bytes were preserved during preparation. The
`preparation.json` additions above describe copying from the then-existing root
license documents. Distribution notices remain in `pack/overrides/`.

## Documentation and recipe review records

The following records describe earlier preparation and review steps, not the current user instructions.

### Documentation review

# ドキュメント精査記録

対象は、このリポジトリの案内・変更履歴・ライセンス通知・履歴資料、および Server Pack に生成される `README-SERVER.md` です。ファイル名と内容の役割、公開読者に必要な情報、実装との一致を確認しました。外部サイトの現在の状態と Minecraft の実機動作は今回の検証対象に含めていません。

## 案内文書を用途別に整理

| ファイル | 精査結果と対応 |
| --- | --- |
| `README.md` | 利用案内、提出手順、認証設定、過去の作業記録が混在。配布概要・導入の入口・文書案内へ書き換え。 |
| `CHANGELOG.md` | 冒頭が特定版の表題で、日本語と英語が混在。文書表題を Changelog、各版を同じ階層に統一し、変更内容を日本語で記載。 |
| `docs/server-setup.md` | README と生成文書の導入情報から新規作成。ZIP の保持、EULA、downloads、データ保存先、world 移行を説明。 |
| `docs/development.md` | README から編集対象・生成方式・検証を移動。固定版と ZIP ハッシュの再現性の限界を保持。 |
| `docs/publishing.md` | README から提出・認証・公開確認を移動。実装にある提出有効化変数の説明を追加し、過去の認証成功と現在の確認を区別。 |
| `CHANGELOG.md` の `0.0.2 submission evidence` | 提出 ID、SHA、回復経緯を記録しており、ファイル名と一致。根拠資料として保持。 |
| `CHANGELOG.md` の `0.0.1 App migration evidence` | 保存資料と歴史的パス、現行入力との区別を説明しており、役割と一致。保持。 |

## ライセンスと配布物内の文書

`LICENSE` と `pack/overrides/LICENSE-Shimae.txt` は同一の MIT 条文です。旧 `LICENSE-SCOPE.txt` の適用範囲説明は、現在の配布物内の通知に保持されています。法的な条文は編集していません。

`pack/overrides/THIRD-PARTY-NOTICES.txt` は旧 `LICENSE-SCOPE.txt` と同じ本文で、個別の第三者名・ライセンスを列挙する通知一覧ではありません。modlist と原プロジェクトのライセンスを参照する一般通知として機能しますが、見出しは「License scope」です。次版でこの見出しを第三者通知に合わせることが改善点です。各 MOD のライセンスを未確認のまま一覧へ補完してはいません。

`pack/overrides/config/better*/` の README 8 件は、各 MOD の設定ディレクトリや JSON の説明で、配置と役割は一致しています。その他の設定用 `.txt` は文書ではなく設定・状態ファイルとして扱いました。

生成される `README-SERVER.md` は導入手順、world 移行、認証を説明しています。一部に作者向けの提出・審査説明もありますが、導入方式の制約は明記されています。現在の本文は `scripts/serverpack.py` にあります。

配布物内の通知・設定 README は `pack/migration.json` の SHA 検証対象です。生成文書の変更も Server Pack のバイト列を変えます。公開済み 0.0.2 と同版の別バイトを作らないため、今回はこれらを保持し、改善は次版の配布内容として扱います。

## 最新 main の履歴統合を反映

PR #10 で `history/` とルートの `LICENSE-SCOPE.txt` が削除され、履歴資料は CHANGELOG に統合されました。今回の PR はその変更を保持し、参照を CHANGELOG の該当節と配布物の通知へ更新しています。公開履歴の英文・原 JSON の引用は根拠資料として保持しています。

現在は CHANGELOG を追加機能・変更内容だけに整理し、提出・移行の根拠資料を [release-history.md](release-history.md) に移しています。上記のCHANGELOGへの統合は過去の整理時点の記録です。

### Coasters recipe review

# Coasters のサバイバル用レシピ

ModPack 0.0.4 / Minecraft 1.21.1 / NeoForge 21.1.243 用。作業台またはインベントリのクラフト欄で、素材を順不同に並べます。いずれも完成品は1個です。

| 完成品 | 素材 |
| --- | --- |
| Booster | 安山岩ケーシング ×1、精密機構 ×1、レッドストーンダスト ×1 |
| Speed Limiter | 安山岩ケーシング ×1、回転速度コントローラー ×1 |
| Seat Locker | 真鍮ケーシング ×1、鉄インゴット ×1、レッドストーンダスト ×1 |

## ModPack への同梱

データパックの正本は `pack/overrides/config/openloader/packs/shimae_coasters/`。Minecraft 1.21.1 のデータパック形式48、単数形の `recipe` ディレクトリと `result.id` を使用します。レシピIDは `shimae:coasters/boost_block`、`shimae:coasters/speed_block`、`shimae:coasters/lock_block` です。

OpenLoader 21.1.5 の使用JARを解析し、`OpenLoaderRepositorySource` が `config/openloader/packs/` を走査し、`PackSelectionConfig(true, TOP, false)` で登録することを確認しました。初回の0.0.4検証ZIPでは旧版の公式説明にある `config/openloader/data/` に置いてしまい、この版で読み込まれませんでした。配置を修正し、リリース番号は本人の指定により0.0.4としています。

OpenLoader が `config/openloader/packs/` のフォルダ形式データパックを読み込み、ゲームインスタンス内の全ワールドに適用します。通常の client export と Server Pack の設定抽出に含まれるため、world を配布したり、各ワールドの datapacks フォルダへ手動コピーしたりする必要はありません。既存環境は更新したパックのMOD参照とconfigを反映して再起動してください。

| 追加MOD | project ID | file ID | 必須依存 |
| --- | --- | --- | --- |
| OpenLoader 21.1.5 | 354339 | 6546293 | Prickle >=21.1、<21.2、NeoForge >=21.1.133、Minecraft >=1.21.1、<1.22 |
| Prickle 21.1.11 | 1023259 | 6961457 | NeoForge >=21.1.61、Minecraft >=1.21.1、<1.22 |

両方を client / server の固定参照に追加。2026-10-10 に CurseForge API と SHA-1 検証済みJARの依存宣言を照合し、現在のゲームとloaderが要件を満たすことを確認しました。追加JARに任意・非互換依存の宣言はありません。

配布先は[OpenLoader公式](https://www.curseforge.com/minecraft/mc-mods/open-loader)、[Prickle公式](https://www.curseforge.com/minecraft/mc-mods/prickle)。JARはリポジトリや配布ZIPに同梱せず、manifestの固定参照から取得します。自作レシピはリポジトリのMITライセンスに従います。

## 検証範囲

既存Create JAR内の素材IDとCoasters JAR内の完成品IDを照合。テストでデータパックの形式とclient export用ステージへの収録、Server Packへの全ファイルの同梱を確認します。本人からインベントリ内の `R` キーでレシピ表示成功の報告を受けました。報告だけではテストしたZIPの版は特定できません。JEI検索で表示されない件は未解決です。実際のクラフト、新規・既存ワールドそれぞれでの自動有効化は未確認です。以前の起動成功報告は今回の追加前のものです。

Coastersの加速・速度制限・座席固定機能そのものやスケジュール命令の挙動は変更しません。

## JEI検索への表示

`config/jei/jei-client.ini` の `showHiddenIngredients = true` を配布設定に反映しています。通常のCreativeタブから収集されないアイテムもJEIの一覧へ追加する設定で、他MODの隠れたアイテムも対象です。MOD ID検索は有効なので、検索欄に `@createcoasters` と入力できます。変更後の実機検索表示は未確認です。既存インスタンスへ更新する場合は、この設定ファイルの反映も確認してください。
