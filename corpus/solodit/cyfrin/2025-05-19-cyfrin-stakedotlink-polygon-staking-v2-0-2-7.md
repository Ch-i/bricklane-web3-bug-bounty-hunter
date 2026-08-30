---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-2-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Potential infinite loop in `PolygonStrategy::unbond` due to insufficient balance
  check
vuln_class: []
---

# Potential infinite loop in `PolygonStrategy::unbond` due to insufficient balance check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** `PolygonStrategy::unbond` function contains a while loop that continues until the entire requested unbonding amount (`toUnbondRemaining`) is processed. However, there is no safeguard to handle a scenario where the total available balance across all vaults is insufficient to satisfy the unbonding request.

```solidity
function unbond(uint256 _toUnbond) external onlyFundFlowController {
    // ...
    uint256 toUnbondRemaining = _toUnbond;

    // ...
    while (toUnbondRemaining != 0) {
        // Process vaults...
        ++i;
        if (i >= vaults.length) i = 0;
        // No check for complete loop iteration without progress
    }
    // ...
}
```
The issue arises because the function assumes that the unbonding amount will always be covered by the total staked amount across all vaults. While this assumption might hold in the current single-strategy setup, it is not guaranteed, especially in a multi-strategy environment.

It is noteworthy that the withdrawal pool, which keeps track of `queuedWithdrawals` that determine the magnitude of `unbonding`, operates at a global level across all strategies.

**Impact:** Although an unlikely scenario for the current single strategy setup, an infinite while loop consumes all available gas.

**Recommended Mitigation:** Consider adding a safety mechanism to detect when the loop has iterated through all vaults without making progress, indicating insufficient funds to satisfy the unbonding request.

```diff solidity

function unbond(uint256 _toUnbond) external onlyFundFlowController {

        while (toUnbondRemaining != 0) {
             // ... code
             if (i >= vaults.length) i = 0;

++       // Add safety check to prevent infinite loop
++        if (i == startingIndex) {
++            // We've gone through all vaults and still have amount to unbond
++            // Process partial unbonding with what we've got so far OR revert
++           break; // or revert if that's more appropriate
++        }

       }
}

```
**Stake.Link:** Resolved in [PR 151](https://github.com/stakedotlink/contracts/pull/151/commits/e138c991bc1f41ec1f33ea62b3459870a29c333e)

**Cyfrin:** Resolved.

\clearpage
