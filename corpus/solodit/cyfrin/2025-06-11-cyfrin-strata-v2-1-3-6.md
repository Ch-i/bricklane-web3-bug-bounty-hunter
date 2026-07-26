---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Missing zero deposit amount validation
vuln_class: []
---

# Missing zero deposit amount validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Unlike `pUSDeDepositor::deposit_USDe`, `pUSDeDepositor::deposit_sUSDe` does not enforce that the deposited amount is non zero:

```solidity
require(amount > 0, "Deposit is zero");
```

A similar case is present when comparing `yUSDeDepositor::deposit_pUSDeDepositor` and `yUSDeDepositor::deposit_pUSDe`.

**Strata:** Fixed in commit [1378b6a](https://github.com/Strata-Money/contracts/commit/1378b6af08e60aaa768693a9332e98dbb4f01776).

**Cyfrin:** Verified.
