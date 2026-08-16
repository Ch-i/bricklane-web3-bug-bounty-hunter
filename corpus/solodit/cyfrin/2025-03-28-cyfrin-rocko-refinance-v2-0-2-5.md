---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-2-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Use named return variables to eliminate redundant local variables and `return`
  statements
vuln_class: []
---

# Use named return variables to eliminate redundant local variables and `return` statements

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Use named return variables to eliminate redundant local variables and `return` statements:
```diff
// _closeLoanPositionAndReturnCollateralBalance L457
-    ) private returns (uint256) {
+    ) private returns (uint256 collateralBalance) {

// L464
-        uint256 collateralBalance;

// L480
-        return collateralBalance;
```

Same idea can be applied to `_collateralBalanceOfAave`, `_getDebtBalanceOfAave`.

**Rocko:** Fixed in commit [751e906](https://github.com/getrocko/onchain/commit/751e906b7c2df6cb587e709b12de25593eb02c75).

**Cyfrin:** Verified.
