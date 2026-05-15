---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Function `claimEffectiveBalance()` may consistently revert, making it impossible
  to complete queue withdrawals
vuln_class: []
---

# Function `claimEffectiveBalance()` may consistently revert, making it impossible to complete queue withdrawals

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** The function attempts to remove the withdrawal at index `0`, while it uses the withdrawal at index `i` to call `completeQueuedWithdrawal()`. Since each withdrawal can only be completed once, the `delayedEffectiveBalanceQueue[]` list will eventually contain withdrawals that have already been completed. When the function tries to complete a withdrawal that has already been completed, it invariably reverts.

```solidity
for (uint256 i; i < delayedEffectiveBalanceQueue.length; i++) {
    IDelegationManager.Withdrawal memory withdrawal = delayedEffectiveBalanceQueue[i];
    if (uint32(block.number) - withdrawal.startBlock > withdrawalDelay) {
        delayedEffectiveBalanceQueue.remove(0); // @audit Remove withdrawal at index 0
        claimedEffectiveBalance += withdrawal.shares[0];
        eigenDelegationManager.completeQueuedWithdrawal(withdrawal, tokens, 0, true); // @audit Complete withdrawal of index i
    } else {
        break;
    }
}
```

**Impact:** The `claimEffectiveBalance()` function consistently reverts, making it impossible to complete queue withdrawals and therefore locking ETH.

**Proof of Concept:** Consider the following scenario:

1. Initially, the `delayedEffectiveBalanceQueue[]` list includes five withdrawals `[a, b, c, d, e]`.
2. The `claimEffectiveBalance()` function is called.
    - In the first loop iteration `i = 0`, withdrawal `a` is removed and completed. The list now becomes `[b, c, d, e]`.
    - In the second loop iteration `i = 1`, withdrawal `b` is removed, but withdrawal `c` is completed. The list now becomes `[c, d, e]`.
    - In the third loop iteration `i = 2`, the function checks withdrawal `e` and assumes the withdrawal delay has not yet been reached. The loop breaks at this point and the function stops.
3. The next time the `claimEffectiveBalance()` function is called.
    - In the first loop iteration `i = 0`, the function tries to remove and complete withdrawal `c`. However, since withdrawal `c` has already been completed, the call to `completeQueuedWithdrawal()` will revert.

**Recommended Mitigation:** Consider using a consistent index for checking, removing and completing withdrawals.

**Casimir:**
Fixed in [35fdf1e](https://github.com/casimirlabs/casimir-contracts/commit/35fdf1e42ad2a38f47028a8468efc0e78e6e7f67)

**Cyfrin:** Verified.
