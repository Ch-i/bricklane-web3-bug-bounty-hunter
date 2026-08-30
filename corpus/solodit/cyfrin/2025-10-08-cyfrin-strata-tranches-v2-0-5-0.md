---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-5-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Remove redundant checks
vuln_class: []
---

# Remove redundant checks

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** The function below behaves the same whether or not that check is present.

* `StrataCDO.sol`
```solidity
// isJrt
154:        if (tranche == address(0)) {
155:            revert InvalidTranche(tranche);
156:        }
```

**Strata:**
Removed redundant check in commit [934be5](https://github.com/Strata-Money/contracts-tranches/commit/934be516bd0e3643d7fe37f19ce62f141281d704).

**Cyfrin:** Verified.
