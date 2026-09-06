---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: In staking contract, rewards distribution can be delayed by front-running distributeGold
  function
vuln_class: []
---

# In staking contract, rewards distribution can be delayed by front-running distributeGold function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** In `TempleGoldStaking` contract, the reward distributer calls `distributeRewards` to by minting available TLGD from the token contract and updates reward rate based on the minted amount.
However, the distribution works only after the distribution cooldown period is passed:
```Solidity
if (lastRewardNotificationTimestamp + rewardDistributionCoolDown > block.timestamp)
    { revert CannotDistribute(); }
```

It uses `lastRewardNotificationTimestamp` as latest updated timestamp, which can be also updated by anyone who calls a public function `distributeGold`.
By front-running this function, it prevents the distributor from updating reward rate.

More seriously, if `distributeGold` is called regularly before the distribution cooldown, rewards distribution can be prevented forever.

**Impact:** Reward distribution can be delayed.

**Recommended Mitigation:** Either making `distributeGold` permissioned or introduce other state variable that represents the latest timestamp of rewards distribution, which is only updated in `distributeRewards` function.

**TempleDAO:** Fixed in [PR 1028](https://github.com/TempleDAO/temple/pull/1028)

**Cyfrin:** Verified
