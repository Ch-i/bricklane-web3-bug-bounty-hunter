---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Users could avoid loss by frontrunning to request unstake
vuln_class: []
---

# Users could avoid loss by frontrunning to request unstake

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** A loss can occur when a validator is slashed, which is reflected in the `finalizeReport()` function. If the `change` is less than 0, this indicates that a loss has occurred. Consequently, the accounting updates the `rewardStakeRatioSum` to decrease the stake value of all users in the `CasimirManager`.

```solidity
} else if (change < 0) {
    uint256 loss = uint256(-change);
    rewardStakeRatioSum -= Math.mulDiv(rewardStakeRatioSum, loss, totalStake);
    latestActiveBalanceAfterFee -= loss;
}
```

However, users can avoid this loss by front-running an unstake request. This is because they can create and fulfill an unstake request within the same `reportPeriod`. If users anticipate a potential loss in the next report (by watching the mempool), they can avoid it by requesting to unstake. The contract processes all unstake requests in a First-In-First-Out (FIFO) queue, meaning reporters must fulfill earlier requests before later ones.

```solidity
function getNextUnstake() public view returns (Unstake memory unstake, bool fulfillable) {
    // @audit Allow to create and fulfill unstake within the same `reportPeriod`
    if (unstakeQueue.length > 0) {
        unstake = unstakeQueue[0];
        fulfillable = unstake.period <= reportPeriod && unstake.amount <= getWithdrawableBalance();
    }
}
```

**Impact:** This can lead to unfairness. The front-runner can avoid losses while retaining all profits.

**Recommended Mitigation:** Consider implementing a waiting or delay period for unstake requests before they can be fulfilled. Do not allow the unstake request to be fulfilled in the same `reportPeriod` in which it was created. Additionally, considering adding a small user fee for unstaking.

**Casimir:**
Fixed in [28baa81](https://github.com/casimirlabs/casimir-contracts/commit/28baa8191a1b5a27d3ee495dee0d993177bf7e5f)

**Cyfrin:** Verified.
