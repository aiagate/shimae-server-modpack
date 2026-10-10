# Create addon review for 0.0.4

Reviewed on 2026-10-10 for Minecraft 1.21.1 / NeoForge 21.1.243. Both additions are pinned in client and server references; totals at this step were 201 / 191. The subsequent [recipe addition](coasters-recipes.md) adds OpenLoader and Prickle, bringing totals to 203 / 193. Existing MOD versions and settings remain unchanged.

| MOD | Project ID | File ID | Filename | SHA-1 |
| --- | --- | --- | --- | --- |
| Create: Design n' Decor 2.2b | 923238 | 8156977 | `Design-n-Decor-1.21.1-2.2b.jar` | `ff5f0411a3d82e15d69b65617128f6d54e818e1b` |
| Create Coasters 2.0 | 1298151 | 8110328 | `createcoasters-2.0.jar` | `e91386c483898d27af9693a346239d810afcc82a` |

The CurseForge API tags both selected files for Minecraft 1.21.1, NeoForge, Client and Server. Downloaded JARs were verified against the API SHA-1 values and their `META-INF/neoforge.mods.toml` files inspected.

- Design n' Decor requires Minecraft exactly 1.21.1, NeoForge >=21.1.200, Create >=6.0.4, Ponder >=0.8, and Flywheel >=1.0.0 and <2.0 on the client.
- Coasters requires Minecraft >=1.21.1 and <1.22, NeoForge >=21, and Create (no version bound). The API dependency list is empty, so the JAR declaration was used.
- The pinned Create 6.0.10 (328085 / 7963363) supplies Flywheel 1.0.6 and Ponder 1.0.82+mc1.21.1 through Jar-in-Jar metadata. These satisfy the new requirements without additional library projects.
- Neither new JAR declares optional or incompatible dependencies. The API dependency lists of all 199 existing pinned files contain no reverse dependency or incompatibility entry targeting either added project. Existing JAR-level reverse constraints were not re-audited in this addition.

This verifies declared dependencies, not runtime API or mixin compatibility with Create, Aeronautics or other addons. The prior client startup report predates these additions. Client startup, world loading and dedicated-server startup with the additions remain unverified; existing metadata warnings in the original update review remain unresolved.

Coasters is designed for creative building: its blocks have no crafting recipes, and its custom schedule instructions can affect survival gameplay. This initial addon step introduced no survival recipes; the subsequent recipe addition is documented separately.

MOD JARs used for inspection are temporary review files outside the repository and are not included in the pack.
