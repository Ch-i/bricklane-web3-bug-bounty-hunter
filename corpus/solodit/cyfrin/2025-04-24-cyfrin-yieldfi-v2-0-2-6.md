---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-2-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Balance check for yield claims in `PerpetualBond::_validate` can be easily
  bypassed
vuln_class: []
---

# Balance check for yield claims in `PerpetualBond::_validate` can be easily bypassed

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In [`PerpetualBond::_validate`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L312-L314), there's a check to ensure that users have a non-zero balance before claiming yield:

```solidity
// Yield claim
require(balanceOf(_caller) > 0, "!bond balance"); // Caller must hold bonds to claim yield
require(accruedRewardAtCheckpoint[_caller] > 0, "!claimable yield"); // Must have claimable yield
```

However, this check can be bypassed by holding a trivial amount, such as 1 wei, of `PerpetualBond` tokens. A more meaningful check would ensure that the user's balance exceeds the `minimumTxnThreshold`, similar to how other parts of the contract enforce value-based thresholds.

Consider updating the balance check to compare against `minimumTxnThreshold` using the bond-converted value:

```diff
- require(balanceOf(_caller) > 0, "!bond balance");
+ require(_convertToBond(balanceOf(_caller)) > minimumTxnThreshold, "!bond balance");
```

Additionally, the second check on `accruedRewardAtCheckpoint[_caller]` is redundant, since [`PerpetualBond::requestYieldClaim`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L374-L378) already performs a value-based threshold check:

```solidity
// Convert yield amount to bond tokens for threshold comparison
uint256 yieldInBondTokens = _convertToBond(claimableYieldAmount);

// Check if the yield claim is worth executing
require(yieldInBondTokens >= minimumTxnThreshold, "!min txn threshold");
```

This makes the `accruedRewardAtCheckpoint` check in `_validate` unnecessary.

**YieldFi:** Fixed in commit [`f0bf88c`](https://github.com/YieldFiLabs/contracts/commit/f0bf88cb51a92a119cdde896c4b0118be1d1a031)

**Cyfrin:** Verified. Balance check removed as the user might still have yield even if they have no tokens (sold/transferred). Yield check in `_validate` is also removed as it's redundant.

\clearpage
