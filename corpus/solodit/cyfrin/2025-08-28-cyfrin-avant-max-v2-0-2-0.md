---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Enable the optimizer
vuln_class: []
---

# Enable the optimizer

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** [Enable the Foundry optimizer](https://dacian.me/the-yieldoor-gas-optimizoor#heading-enabling-the-optimizer) in `foundry.toml`:
```diff
+ optimizer = true
+ optimizer_runs = 1_000
```

**Avant:**
Fixed in commit [871140d](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/871140d5175f2f7ca7de7be960b834eb1f671206).

**Cyfrin:** Verified.
