---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: '`RewardsDistributor` doesn''t correctly handle deposits of fee-on-transfer
  incentive tokens'
vuln_class: []
---

# `RewardsDistributor` doesn't correctly handle deposits of fee-on-transfer incentive tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** `the kenneth` stated in telegram that Fee-On-Transfer tokens are fine to use as incentive tokens with `RewardsDistributor`, however when receiving Fee-On-Transfer tokens and storing the reward amount the accounting does not account for the fee deducted from the transfer amount in-transit, [for example](https://github.com/SolidlyV3/v3-rewards/blob/6dfb435392ffa64652c8f88c98698756ca80cf28/contracts/RewardsDistributor.sol#L348-L359):

```solidity
function _depositLPIncentive(
    StoredReward memory reward,
    uint256 amount,
    uint256 periodReceived
) private {
    IERC20(reward.token).safeTransferFrom(
        msg.sender,
        address(this),
        amount
    );

    // @audit stored `amount` here will be incorrect since it doesn't account for
    // the actual amount received after the transfer fee was deducted in-transit
    _storeReward(periodReceived, reward, amount);
}
```

**Impact:** The actual reward calculation is done off-chain and is outside the audit scope nor do we have visibility of that code. But events emitted by `RewardsDistributor` and the stored incentive token deposits in `RewardsDistributor::periodRewards` use incorrect amounts for Fee-On-Transfer incentive token deposits.

**Recommended Mitigation:** In `RewardsDistributor::_depositLPIncentive` & `depositVoteIncentive`:
* read the `before` transfer token balance of `RewardsDistributor` contract
* perform the token transfer
* read the `after` transfer token balance of `RewardsDistributor` contract
* calculate the difference between the `after` and `before` balances to get the true amount that was received by the `RewardsDistributor` contract accounting for the fee that was deducted in-transit
* use the true received amount to generate events and write the received incentive token amounts to `RewardsDistributor::periodRewards`.

Also note that `RewardsDistributor::periodRewards` is never read in the contract, only written to. If it is not used by off-chain processing then consider removing it.

**Solidly:**
Fixed in commit [be54da1](https://github.com/SolidlyV3/v3-rewards/commit/be54da1fea0f1f6f3e4c6ee20464b962cbe2077f).

**Cyfrin:**
Verified.
