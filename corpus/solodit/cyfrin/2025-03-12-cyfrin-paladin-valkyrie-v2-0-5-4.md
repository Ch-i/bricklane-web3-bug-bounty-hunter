---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-5-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Cache storage reads in `TimeWeightedIncentiveLogic`
vuln_class: []
---

# Cache storage reads in `TimeWeightedIncentiveLogic`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** Unlike the other logic contracts, `TimeWeightedIncentiveLogic` does not currently cache the reward distribution rate read from storage.

**Recommended Mitigation:**
```diff
function _depositRewards(
    IncentivizedPoolId id,
    address token,
    uint256 amount,
    uint256 duration,
    uint256 requiredDuration,
    RewardType rewardType
) internal {
    ...
    if (endTimestampCache < block.timestamp) {
        ...
    } else {
        if (msg.sender != distributionManagers[id][token]) revert CallerNotManager();
        if (rewardType != distributionRewardTypes[id][token]) revert CannotChangeParameters();
        if (requiredDuration != distributionRequiredDurations[id][token]) revert CannotChangeParameters();

        // Calculates the remianing duration left for the current distribution
        uint256 remainingDuration = endTimestampCache - block.timestamp;
        if (remainingDuration + duration < MIN_DURATION) revert InvalidDuration();
        // And calculates the new duration
        uint256 newDuration = remainingDuration + duration;

        // Calculates the leftover rewards from the current distribution
--    uint256 leftoverRewards = _state.ratePerSec * remainingDuration;
++    uint96 ratePerSecCache = _state.ratePerSec;
++    uint256 leftoverRewards = ratePerSecCache * remainingDuration;

        // Calculates the new rate
        uint256 newRate = (amount + leftoverRewards) / newDuration;
--      if (newRate < _state.ratePerSec) revert CannotReduceRate();
++      if (newRate < ratePerSecCache) revert CannotReduceRate();

        // Stores the new reward distribution parameters
        _state.ratePerSec = newRate.toUint96();
        _state.endTimestamp = (block.timestamp + newDuration).toUint32();
        _state.lastUpdateTime = (block.timestamp).toUint32();
    }

    IncentiveManager(incentiveManager).addPoolIncentiveSystem(id);
    // Sync pool total liquidity if not already done
    if(!poolSynced[id]) {
        _syncPoolLiquidity(id);
        poolSynced[id] = true;
    }

    emit RewardsDeposited(id, token, amount, duration);
}
```

**Paladin:** Fixed by commit [`075c846`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/075c84618e1f94b17ad10afeb6d77ea101195871).

**Cyfrin:** Verified. The rate is now cached.
