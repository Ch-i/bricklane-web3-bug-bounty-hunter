---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-03-rush-trading-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-02-03T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-03-Rush-Trading.md
tags:
- firm:hexens
- report:2025-02-03-rush-trading
title: '[RUSH1-1] Rewards in StakingRewards are lost if total supply is zero'
vuln_class: []
---

# [RUSH1-1] Rewards in StakingRewards are lost if total supply is zero

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2025-02-03-Rush-Trading.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-03-Rush-Trading.md)_

---

**Severity:** Low

**Path:** StakingRewards.sol:rewardPerToken#L90-L96

**Description:** The function rewardPerToken calculates the current amount of reward tokens per share inside of the StakingRewards. It is calculated using the initially set rewardRate and the delta time of lastTimeRewardApplicable() and lastUpdateTime. However, it also has an edge case if the total supply is zero, where it directly returns the rewardPerTokenStored. 

This function is called in the modifier updateReward where the lastUpdateTime is also set to the current applicable time. As a result, the rewards that were accumulated inside of that time frame would be lost and unaccounted for.

It is correct that the next depositing user would not get these rewards, but now those tokens would be stuck in the contract and lost forever.

This case will almost certainly happen at the start of the StakingRewards, where there would be some time without any supply, while the reward rate immediately starts.
```
function rewardPerToken() public view override returns (uint256) {
    if (totalSupply == 0) {
        return rewardPerTokenStored;
    }
    return rewardPerTokenStored
        + Math.mulDiv((lastTimeRewardApplicable() - lastUpdateTime) * rewardRate, 1e18, totalSupply);
}
```

**Remediation:**  We see two options:

1. Introduce a sweep function that can only be called by an authorised role and only after the staking period has finished.

2. Divide the unaccounted token amounts linearly over the remaining duration and add to the rewardRate.

**Status:**   Acknowledged



- - -
