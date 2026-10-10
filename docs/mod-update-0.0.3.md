# MOD update review for 0.0.3

Reviewed on 2026-10-10 using the CurseForge Core API and downloaded JAR metadata. Minecraft remains 1.21.1 and NeoForge remains 21.1.243. This original update review covers 199 client references and 189 server references. The subsequent two-MOD addition brought these to 201 / 191; [recipe distribution](coasters-recipes.md) subsequently adds OpenLoader and Prickle for totals of 203 / 193; see [Create addon review](create-addons-0.0.4.md).

Updated 88 client references, including 84 server references. Only available files explicitly tagged for Minecraft 1.21.1 and NeoForge were considered; release files do not move to beta/alpha. Projects already using previews may stay at their existing release channel. Shader references are unchanged. No external dependency projects were added.

## Dependency verification

- Downloaded current and candidate JARs and verified their CurseForge SHA-1 hashes. Read NeoForge/Forge MOD metadata recursively, including bundled Jar-in-Jar dependencies.
- Compared required, installed optional, and incompatible MOD version ranges separately for client and server using Maven ComparableVersion. Checked Minecraft/NeoForge constraints and reverse dependencies from unchanged MODs.
- Checked that each bundled library group/artifact has an available version satisfying all declared Jar-in-Jar ranges. Both the baseline and updated selections have no empty intersections.
- JEI now bundles mezz_config 0.5.12, satisfying its new required dependency without a new project reference. Create Aeronautics updates its bundled components together. MineColonies/Structurize, Apotheosis/Apothic Enchanting, and Sophisticated Core/Storage/Backpacks move together.
- This is static metadata verification. It does not verify APIs, mixins, world migration, configuration migrations, or game/server startup.

## Candidates limited by dependencies

- Quark: use 4.1-486 (9041023). Latest 4.1-487 requires NeoForge >=21.1.252.
- Supplementaries: use 3.8.10 (8668121). Newer candidates require NeoForge >=21.1.247; the current loader is 21.1.243.
- Create: Bits ’n’ Bobs: keep 0.0.44 (7591460). Every newer eligible candidate introduces unsatisfied dependencies or incompatibilities. Latest 2.3.5 requires azimuth >=1.4.6 and struts >=1.0.0 and forbids the installed TFMG 1.2.0 (range <=1.2.2).
- Construction Wands Revived: keep 4.2.2. The newer upload declares 4.0.7, which would downgrade the MOD.

## Existing metadata warnings

The original pack already declares Minecraft ranges excluding 1.21.1 in JEI, Iris, TownTalk, Create Sophisticated Backpacks Compat, and the adventure_platform_neoforge library bundled by TabTPS. These produce nine client/server dependency warnings before and after this update, with identical owner, target, range, and selected target version. No new warning was introduced. These declarations must be resolved against NeoForge runtime behavior or upstream fixes before claiming complete runtime compatibility; dependencies were not forcibly overridden.

## Fixed reference changes

| Project | MOD | Previous file ID | Selected file ID | Selected filename |
| --- | --- | --- | --- | --- |
| 225738 | MmmMmmMmmMmm (Target Dummy) | 7943676 | 8903254 | `dummmmmmy-1.21-2.1.2-neoforge.jar` |
| 238222 | Just Enough Items (JEI) | 8392171 | 9068136 | `jei-1.21.1-neoforge-19.57.0.451.jar` |
| 243121 | Quark | 8420966 | 9041023 | `Quark-4.1-486.jar` |
| 245506 | MineColonies | 8138370 | 9058295 | `minecolonies-1.1.1403-1.21.1.jar` |
| 245755 | Waystones | 8498220 | 8969751 | `waystones-neoforge-1.21.1-21.1.46.jar` |
| 263420 | Xaero's Minimap | 8449819 | 9067173 | `xaerominimap-neoforge-1.21.1-26.6.0.jar` |
| 274259 | Carry On | 8383188 | 8512888 | `carryon-neoforge-1.21.1-2.2.6.13.jar` |
| 283644 | Placebo | 8463693 | 9077763 | `Placebo-1.21.1-9.9.3.jar` |
| 298744 | Structurize | 8138382 | 8610535 | `structurize-1.0.832-1.21.1.jar` |
| 308663 | Snow! Real Magic! ⛄ (Neo/Forge) | 8321970 | 8988910 | `SnowRealMagic-1.21.1-NeoForge-12.2.3.jar` |
| 312359 | Dawn Of Time | 8004650 | 9031116 | `dawnoftimebuilder-neoforge-1.21.1-1.6.7.jar` |
| 313970 | Apotheosis | 8525273 | 8993983 | `Apotheosis-1.21.1-8.9.0.jar` |
| 317780 | Xaero's World Map | 8449921 | 9067277 | `xaeroworldmap-neoforge-1.21.1-1.47.0.jar` |
| 324717 | Jade 🔍 | 7545219 | 8591319 | `Jade-1.21.1-NeoForge-15.10.6.jar` |
| 326652 | Cupboard | 8481114 | 8889050 | `cupboard-1.21.1-4.2.jar` |
| 340583 | YUNG's Better Caves (Forge/NeoForge) | 6939522 | 8806071 | `YungsBetterCaves-1.21.1-NeoForge-3.1.6.jar` |
| 378609 | Tom's Simple Storage Mod | 8501301 | 8769956 | `toms_storage-1.21-2.4.2.jar` |
| 388172 | GeckoLib | 8350073 | 8893490 | `geckolib-neoforge-1.21.1-4.9.3.jar` |
| 394468 | Sodium | 8382328 | 8756580 | `sodium-neoforge-0.8.13+mc1.21.1.jar` |
| 398521 | Farmer's Delight | 8083481 | 8765184 | `FarmersDelight-1.21.1-1.3.4.jar` |
| 404465 | FTB Library (NeoForge) | 8438216 | 9008089 | `ftb-library-neoforge-2101.1.37.jar` |
| 412082 | Supplementaries | 8501612 | 8638261 | `supplementaries-1.21.1-3.8.10-neoforge.jar` |
| 422301 | Sophisticated Backpacks | 8503096 | 9083940 | `sophisticatedbackpacks-1.21.1-3.26.9.2195.jar` |
| 441647 | FramedBlocks | 8349218 | 8780141 | `FramedBlocks-10.6.2.jar` |
| 448233 | Entity Culling Fabric/Forge | 8287097 | 9100286 | `entityculling-neoforge-1.11.3-mc1.21.1.jar` |
| 454372 | SuperMartijn642's Core Lib | 7783425 | 9083552 | `supermartijn642corelib-1.1.25-neoforge-mc1.21.jar` |
| 495476 | Puzzles Lib | 8251525 | 9100581 | `puzzleslib-v21.1.63-mc1.21.1+neoforge.jar` |
| 499980 | Moonlight Lib | 8495469 | 9066398 | `moonlight-1.21.1-3.7.1-neoforge.jar` |
| 508933 | Distant Horizons: A Level of Detail mod | 8389148 | 9004764 | `DistantHorizons-3.3.3-1.21.1-fabric-neoforge.jar` |
| 521480 | Skin Layers 3D | 8274824 | 8906440 | `skinlayers3d-neoforge-1.11.3-mc1.21.1.jar` |
| 531761 | Balm | 8424824 | 8969738 | `balm-neoforge-1.21.1-21.0.66.jar` |
| 533097 | Concurrent Chunk Management Engine | 8480771 | 8896937 | `c2me-neoforge-mc1.21.1-0.4.0-alpha.0.122.jar` |
| 551586 | L_Ender 's Cataclysm | 8364209 | 8931182 | `L_Ender's Cataclysm 1.21.1-3.33.jar` |
| 558998 | Rechiseled | 8301793 | 8875899 | `rechiseled-1.2.6-neoforge-mc1.21.jar` |
| 610492 | Another Furniture | 7355747 | 8955672 | `another_furniture-neoforge-4.0.3.jar` |
| 618298 | Sophisticated Core | 8503041 | 9083874 | `sophisticatedcore-1.21.1-1.5.7.2381.jar` |
| 619320 | Sophisticated Storage | 8503122 | 9083992 | `sophisticatedstorage-1.21.1-1.6.2.2159.jar` |
| 656977 | MVS - Moog's Voyager Structures | 8370969 | 8970306 | `MoogsVoyagerStructures-universal-1.21-5.1.3.jar` |
| 676721 | Create Aeronautics | 8240058 | 8763471 | `create-aeronautics-bundled-1.21.1-1.3.2.jar` |
| 686836 | Tectonic | 8360847 | 8855043 | `tectonic-3.0.28-neoforge-21.1.jar` |
| 790626 | ModernFix | 8459650 | 9101836 | `modernfix-neoforge-5.27.26+mc1.21.1.jar` |
| 817423 | AzureLib | 8367232 | 9107208 | `azurelib-neo-1.21.1-3.1.19.jar` |
| 820977 | Create: Central Kitchen | 8221844 | 9104646 | `create-central-kitchen-2.6.2b.jar` |
| 827507 | Stylecolonies | 8422813 | 8782133 | `stylecolonies-1.15.59-1.21.1.jar` |
| 854949 | Fusion (Connected Textures) | 8479774 | 9070353 | `fusion-1.3.16-neoforge-mc1.21.1.jar` |
| 896746 | Amendments | 8415430 | 8825641 | `amendments-1.21-2.1.10-neoforge.jar` |
| 898963 | Apothic Attributes | 8502288 | 9006294 | `ApothicAttributes-1.21.1-2.11.0.jar` |
| 936015 | Lithostitched | 8378498 | 8944659 | `lithostitched-1.8.0-neoforge-21.1.jar` |
| 947914 | Create: Connected | 8299240 | 8777573 | `create_connected-1.3.3-mc1.21.1.jar` |
| 960209 | Valarian Conquest | 7757180 | 8729162 | `valarian_conquest-4.2.2-neoforge-1.21.1.jar` |
| 968398 | Create: Copycats+ | 7251823 | 8822348 | `copycats-3.0.9+mc.1.21.1-neoforge.jar` |
| 1007872 | Create: Let The Adventure Begin | 8281653 | 8608393 | `create_ltab-4.1.0.jar` |
| 1015100 | YUNG's API (NeoForge) [1.20.4-1.21.1 ONLY] | 6715463 | 8894736 | `YungsApi-1.21.1-NeoForge-5.1.9.jar` |
| 1063926 | Apothic Enchanting | 8469450 | 9095862 | `ApothicEnchanting-1.21.1-1.6.4.jar` |
| 1140577 | Cable Facades | 8271740 | 8734901 | `cable_facades-1.21.1-NeoForge-2.1.4.jar` |
| 1216624 | Create: Dragons Plus | 8219463 | 8900055 | `CreateDragonsPlus-1.11.9.jar` |
| 1238567 | Sophisticated Backpacks Create Integration | 8398818 | 9074505 | `sophisticatedbackpackscreateintegration-1.21.1-0.2.2.188.jar` |
| 1263531 | Underlay | 8415125 | 8956338 | `underlay-1.0.5-neoforge-mc1.21.1.jar` |
| 1281310 | Jauml | 8316937 | 9020151 | `jauml-neoforge-1.21.1-2.3.1.jar` |
| 1281336 | Create: Hypertubes | 8281768 | 8541877 | `create_hypertube-0.6.0-NEOFORGE.jar` |
| 1307924 | Immersive Gateways | 8235643 | 8852736 | `immersive_gateways-neoforge-0.0.7.jar` |
| 1312371 | Sable | 8263584 | 9043865 | `sable-neoforge-1.21.1-2.0.6.jar` |
| 1317252 | Create: Blocks & Bogies | 7471348 | 8723463 | `create_bb-1.0.8-1.21.1.jar` |
| 1332665 | CreateColonies | 8425170 | 8956260 | `createcolonies-2.0.7.jar` |
| 1337167 | Moog's Structure Lib (moogs_structures) | 8463709 | 9047179 | `MoogsStructureLib-neoforge-1.21.1-3.4.2.jar` |
| 1426984 | VS / Sable Hose Connectors | 8333129 | 9113896 | `VS-Sable-HoseConnectors-0.1.9-1.21.1.jar` |
| 1443327 | Create: Electro Energetics | 8345582 | 9058907 | `electroenergetics-1.21.1-1.1.3.jar` |
| 1489732 | CBC Enchanced Shells [Create Big Cannons] | 8470471 | 8853805 | `CBCmoreshells-1.4.0.jar` |
| 1499714 | Much More Dungeons | 8006651 | 8737899 | `muchmoredungeons-neoforge-1.21.1-1.2.0.jar` |
| 1511282 | Create: Stats & Power | 8376124 | 9074215 | `create_stats-1.15.0.jar` |
| 1521349 | create aeronautics：toolgun | 8466588 | 8701394 | `create_aeronautics_toolgun-0.3.6.jar` |
| 1522473 | Create: Aeroworks | 8409091 | 8743051 | `aeroworks-1.5.0.jar` |
| 1524471 | Waystones: Sable (Create Aeronautics Addon) | 8404634 | 8632751 | `waystonessable-1.0.7.jar` |
| 1526086 | Create: Pipes'n Physics | 8380829 | 8849438 | `pipesnphysics-3.2.1.jar` |
| 1528764 | Climbable Ropes for Create Aeronautics | 8464450 | 8976817 | `climbable_ropes-2.1.4.jar` |
| 1529882 | Create Aeronautics: Throwable Rope Connector | 8368780 | 8618590 | `create_aeronautics_throwable_rope_connector-0.4.3.jar` |
| 1532314 | DECI-lib | 8083393 | 8592815 | `decilib-neoforge-1.1.5+1.21.1.jar` |
| 1533137 | Create  Deep Seas | 8268622 | 9042070 | `create_submarine-3.3.0.jar` |
| 1533254 | GpuShift | 8481512 | 8881861 | `gpushift-universal-1.21.1-1.2.8-bugfix.2.jar` |
| 1533966 | Illager Structures | 8050151 | 8638957 | `illagerstructures-neoforge-1.21.1-0.1.2.jar` |
| 1534320 | Trial Guardians | 8211494 | 8641826 | `trial_guardians-neoforge-2.0.0+1.21.1.jar` |
| 1537420 | Create Aeronautics: Automated Logistics | 8348610 | 8673342 | `create_aeronautics_automated_logistics-0.6.2.jar` |
| 1537945 | Create Aeronautics: Gadgets & Gizmos | 8486860 | 9110305 | `gadgets-and-gizmos-bundled-V1.2.8.jar` |
| 1542803 | MVSI - Moog's Voyager Structures Integrated | 8094325 | 8661797 | `MoogsVoyagerStructuresIntegrated-neoforge-1.21.1-2.0.1.jar` |
| 1548056 | Create Aeronautics: Transmission & Linkage | 8264158 | 8790451 | `create_aeronautics_transmission_linkage-0.2.8.jar` |
| 1553375 | Cataclysm's Rise | 8241900 | 8883036 | `cataclysm_rise-1.1.3.jar` |
| 1571184 | Create: Steel armor blocks Recipes | 8388122 | 8967641 | `sab_tfmg_compat-1.1.0.jar` |
| 1591852 | Voxy Server Side Horizon | 8479554 | 8753475 | `vss-0.2.12-neoforge-1.21.1.jar` |

## Distribution validation

- All 79 existing unit tests pass; Python compilation and whitespace checks pass.
- Built client and server ZIPs with the pinned packwiz module and verified Go 1.27.2 toolchain/module checksum.
- Independently rebuilt both ZIPs and verified identical fixed references and override contents.
- Submission dry-run verified both ZIPs and receipts without uploading.
- Release metadata is 0.0.3. No game/server startup or publication was performed.

## User-reported client startup verification (2026-10-10)

The user confirmed successful installation after restarting their PC and then confirmed client startup. The provided log excerpt covers 13:40:14–13:40:17 JST: Minecraft 1.21.1, NeoForge 21.1.243, Java 21.0.12.1, and detection of updated MODs including Sodium 0.8.13, Apotheosis 8.9.0, and Create Aeronautics 1.3.2. No ERROR/FATAL entries appear in this excerpt. Sodium reports its NVIDIA_THREADED_OPTIMIZATIONS_BROKEN workaround. The excerpt ends during MOD discovery, so successful startup is user-reported; it does not independently establish completed loading, world loading, or dedicated-server startup. Private raw logs are not committed.
