# Shimae Server Modpack 0.0.2

- Build the client with pinned packwiz from repository-owned references/settings. The 199 pinned references and existing settings are unchanged.
- Replace the bundled server distribution with a lightweight manifest-based installer input for standard itzg AUTO_CURSEFORGE: 189 server references, 309 settings, no MOD JARs.
- Generate, verify and publish client/Additional Server Pack through Actions with durable duplicate prevention.
- Minecraft 1.21.1 / NeoForge 21.1.243. Runtime testing of this installer distribution has not been performed.

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

## Previous release

# Shimae Server Modpack 0.0.1

- Minecraft 1.21.1 / NeoForge 21.1.243、クライアント199参照。App出力のmanifestとmodlistを維持。
- TFC、TFC Offset Smoker、Bonsaiは収録せず、PatchouliとApotheosis関連ライブラリを保持。
- 新しいApp出力の有効な設定を採用。Apotheosis/Enchanting連携設定3件と既存設定14件の差分を保持。
- 提出候補では不要なベンチマーク、機器fingerprint、Chunky作業状態、バックアップ、Bonsai残存設定11件を除外し、ライセンス文書2件を付属。
- 原本ZIPは変更せず、manifest、modlist、残した設定本文はバイト一致する整理コピーを使用。

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
