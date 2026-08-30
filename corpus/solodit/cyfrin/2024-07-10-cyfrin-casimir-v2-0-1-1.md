---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Multiple unstake requests can cause denial of service because withdrawn balance
  is not adjusted after every unstake request is fulfilled
vuln_class: []
---

# Multiple unstake requests can cause denial of service because withdrawn balance is not adjusted after every unstake request is fulfilled

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** A `while` loop runs over a specific number of unstake requests, and in every iteration, it checks if an unstake request is fulfillable. If it is, the unstaked amount is transferred back to the staker who requested unstaking. Honoring every unstaking request reduces the effective ETH balance in the manager, however, the `getNextUnstake` function continues to use the stale `withdrawnEffectiveBalance` while checking if the next unstake request is fulfillable.

In fact, `withdrawnEffectiveBalance` is adjusted only after the completion of the `while` loop.
```solidity
function fulfillUnstakes(uint256 count) external {
    //@note called when report status is in fulfilling unstakes
    onlyReporter();

    if (reportStatus != ReportStatus.FULFILLING_UNSTAKES) {
        revert ReportNotFulfilling();
    } //@note ok => report has to be in this state

    uint256 unstakedAmount;
    while (count > 0) {
        count--;

>       (Unstake memory unstake, bool fulfillable) = getNextUnstake(); //@audit uses the stale withdrawn balance
        if (!fulfillable) {
            break;
        }

        unstakeQueue.remove(0);
>       unstakedAmount += unstake.amount; //@audit unstakedAmount is increased here
>       fulfillUnstake(unstake.userAddress, unstake.amount); //@audit even after ETH is transferred, withdrawn balance is same
    }

    (, bool nextFulfillable) = getNextUnstake();
    if (!nextFulfillable) {
        reportStatus = ReportStatus.FINALIZING;
    }

>   if (unstakedAmount <= withdrawnEffectiveBalance) { //@audit withdrawn balance and unassigned balance adjustment happens here
        withdrawnEffectiveBalance -= unstakedAmount;
    } else {
        uint256 remainder = unstakedAmount - withdrawnEffectiveBalance;
        withdrawnEffectiveBalance = 0;
        unassignedBalance -= remainder;
    }

    unstakeQueueAmount -= unstakedAmount;
}
```
**Impact:** The `fulfillUnstakes()` function may fulfill more requests than the allowable withdrawable balance. This could cause the function to overflow and revert at the end.

**Proof of Concept:** **Recommended Mitigation:**
Consider updating `withdrawnEffectiveBalance` after an unstake request has been fulfilled by the `fulfillUnstakes()` function.

**Casimir:**
Fixed in [9f8920f](https://github.com/casimirlabs/casimir-contracts/commit/9f8920f483e5505726e3011132246bfcbea2e629)

**Cyfrin:** Verified.
