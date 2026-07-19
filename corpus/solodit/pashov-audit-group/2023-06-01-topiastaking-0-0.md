---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-topiastaking-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-topiastaking
title: '[C-01] Rewards calculation error will result in 0 rewards for users'
vuln_class: []
---

# [C-01] Rewards calculation error will result in 0 rewards for users

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-TopiaStaking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md)_

---

**Description**

The formula to calculate rewards in `getUserStakeReward` is the following:

```solidity
rewardsPerWeight_.accumulated = (rewardsPerWeight_.accumulated +
    (unaccountedTime * rewardsPerWeight_.rate) / rewardsPerWeight_.totalWeight).toUint96();
```

It is the same in `updateRewardsPerWeight`. The problem with this code is that `(unaccountedTime * rewardsPerWeight_.rate) / rewardsPerWeight_.totalWeight` will round down to zero almost always. Since both `totalWeight` and `rate` are measured in 18 decimals tokens (expected), then as more users stake it is highly likely that the `totalWeight` will grow much more than the static `rate`. The `unaccountedTime` variable just holds how many seconds have passed since the last stake/unstake event, which will always be a pretty small number (1 day is 86400 seconds, which is a small, 5 digit number). Now when `(unaccountedTime * rewardsPerWeight_.rate)` is smaller than `rewardsPerWeight_.totalWeight` this math will round down to zero and `rewardsPerWeight_.accumulated` will stay the same value, meaning no new rewards will be accumulated to be distributed to users anymore.

**Recommendations**

In both `getUserStakeReward` and `updateRewardsPerWeight` change code like:

```diff
- (unaccountedTime * rewardsPerWeight_.rate) / rewardsPerWeight_.totalWeight
+ (unaccountedTime * rewardsPerWeight_.rate).divWadDown(rewardsPerWeight_.totalWeight)
```

And also in `getUserStakeReward` change code like:

```diff
- return getUserStakeWeight(userStake) * (rewardsPerWeight_.accumulated - userStake.checkpoint);
+ return getUserStakeWeight(userStake).mulWadDown(rewardsPerWeight_.accumulated - userStake.checkpoint);
```

By using [FixedPointMathLib from Solmate](https://github.com/transmissions11/solmate/blob/main/src/utils/FixedPointMathLib.sol).

**Discussion**

**pashov:** Fixed.
