---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`AccountableYield::_accruePenalties` includes `accruedPenalties` in the penalty
  base, charging compound interest instead of simple interest'
vuln_class: []
---

# `AccountableYield::_accruePenalties` includes `accruedPenalties` in the penalty base, charging compound interest instead of simple interest

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** Each penalty increment is computed as a fraction of `_totalAssets`:

```solidity
uint256 penaltyAmount =
    _totalAssets(vault).mulDiv(lateInterestPenalty_ * penaltyTime, DAYS_1_SECONDS * BASIS_POINTS);
...
accruedPenalties += penaltyAmount;
```

and `_totalAssets` includes `accruedPenalties`:

```solidity
return IAccountableVault(vault_).totalAssets() + deployedAssets + accruedPenalties;
```

Because the base includes already-accrued penalties, each call charges interest on top of prior penalties, i.e. compound interest rather than simple interest on the outstanding debt. `_accruePenalties` runs frequently: on `borrow`, `repay`, `publishRate`, `updateTerms`, and on `updateLateStatus`, which the vault invokes after every deposit, mint, and redeem. The more often it runs, the closer the growth approaches continuous compounding. `lateInterestPenalty` has no upper bound in `setTerms` / `updateTerms`, so at high rates the divergence is large: at 10%/day over 30 days, simple interest is 300% of the base while continuous compounding is roughly 1,900%.

**Impact:** Penalties grow super-linearly with time and accrual frequency, inflating `accruedPenalties`, `_totalAssets`, and the share price beyond the intended simple-interest schedule, so depositors entering at the inflated price are mispriced and absorb the collapse whnowen the borrower defaults and the phantom penalties are written off.

**Recommended Mitigation:** Compute the penalty increment from a base that excludes prior penalties, so accrual is simple interest on the principal:

```diff
+    // Simple interest on the principal base, excluding already-accrued penalties
+    uint256 penaltyBase = IAccountableVault(vault).totalAssets() + deployedAssets;
     uint256 penaltyAmount =
-        _totalAssets(vault).mulDiv(lateInterestPenalty_ * penaltyTime, DAYS_1_SECONDS * BASIS_POINTS);
+        penaltyBase.mulDiv(lateInterestPenalty_ * penaltyTime, DAYS_1_SECONDS * BASIS_POINTS);
```
**Accountable:** Fixed in commit [`c54cb88`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/c54cb88b1c6fb3c757eea876a74534d4725903b7)

**Cyfrin:** Verified. The penalty base now excludes `accruedPenalties`, so penalties accrue as simple interest rather than compounding.


\clearpage
