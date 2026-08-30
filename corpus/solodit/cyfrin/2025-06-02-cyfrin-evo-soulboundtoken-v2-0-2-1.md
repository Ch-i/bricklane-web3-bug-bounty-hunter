---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Enable the optimizer
vuln_class: []
---

# Enable the optimizer

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** [Enable the optimizer](https://dacian.me/the-yieldoor-gas-optimizoor#heading-enabling-the-optimizer) in `foundry.toml`.

Gas results:
```diff
{
-  "addToBlacklist": "31090"
+  "addToBlacklist": "30691"

-  "addToWhitelist": "28754"
+  "addToWhitelist": "28392"

-  "batchAddToBlacklist": "60282"
+  "batchAddToBlacklist": "59482"

-  "batchAddToWhitelist": "55790"
+  "batchAddToWhitelist": "54997"

-  "batchMintAsAdmin": "252102"
+  "batchMintAsAdmin": "248867"

-  "batchRemoveFromBlacklist": "5289"
+  "batchRemoveFromBlacklist": "4594"

-  "batchRemoveFromWhitelist": "5305"
+  "batchRemoveFromWhitelist": "4677"

-  "batchSetAdmin": "28090"
+  "batchSetAdmin": "27412"

-  "mintAsAdmin": "130754"
+  "mintAsAdmin": "129447"

-  "mintAsWhitelisted": "135623"
+  "mintAsWhitelisted": "132292"

-  "mintWithTerms": "142281"
+  "mintWithTerms": "137638"

-  "removeFromBlacklist": "2516"
+  "removeFromBlacklist": "2203"

-  "removeFromWhitelist": "2634"
+  "removeFromWhitelist": "2254"

-  "setAdmin": "27187"
+  "setAdmin": "26677"

-  "setContractURI": "29118"
+  "setContractURI": "26842"

-  "setFeeFactor": "26075"
+  "setFeeFactor": "25666"

-  "setWhitelistEnabled": "7175"
+  "setWhitelistEnabled": "6902"

-  "withdrawFees": "14114"
+  "withdrawFees": "13462"
}

```

**Evo:**
Fixed in commit [b4fcadb](https://github.com/contractlevel/sbt/commit/b4fcadbd9c5684cc4e3b1ee3c39f72c406aaf658).

**Cyfrin:** Verified.
