---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Disable initializers on upgradeable contracts
vuln_class: []
---

# Disable initializers on upgradeable contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Disable initializers on upgradeable contracts:
* `yUSDeVault`
* `yUSDeDepositor`
* `pUSDeVault`
* `pUSDeDepositor`

```diff
+    /// @custom:oz-upgrades-unsafe-allow constructor
+    constructor() {
+       _disableInitializers();
+    }
```

**Strata:** Fixed in commit [49060b2](https://github.com/Strata-Money/contracts/commit/49060b25230389feff54597a025a7aa129ceb9f3).

**Cyfrin:** Verified.
