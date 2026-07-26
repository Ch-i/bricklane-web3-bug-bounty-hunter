---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-0-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Lack of Epoch End Block Consideration in `pendingRewards` Function
vuln_class: []
---

# Lack of Epoch End Block Consideration in `pendingRewards` Function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Medium

**Status**:  Unresolved


**Source**: LpNFTPool.sol

**Description**: 

The `pendingRewards` function calculates the pending rewards for a staking position without considering the end of the epoch block `(endOfEpochBlock)`. This omission can lead to the calculation of rewards beyond the intended reward distribution period, potentially resulting in over-distribution of rewards. The function recalculates `accRewardsPerShare` based on the current block timestamp, last reward time, reserve, and pool emission rate without checking if the current period is within the active epoch defined for reward distribution.

**Recommendation**: 

To ensure that rewards are accurately calculated and distributed within the designated epochs, it is recommended to incorporate a check for the `endOfEpochBlock` within the `pendingRewards` function. This check should ensure that rewards are only calculated up to the end of the active epoch. If the current block number exceeds the `endOfEpochBlock`, the calculation should use the `endOfEpochBlock` as the upper limit for the rewards period. This modification will prevent the potential over-distribution of rewards and ensure that the reward distribution aligns with the intended epochs set by the contract owner or protocol.


```solidity
function pendingRewards(uint256 tokenId) external view returns (uint256) {
    StakingPosition storage position = _stakingPositions[tokenId];

    uint256 accRewardsPerShare = _accRewardsPerShare;
    (,,uint256 lastRewardTime, uint256 reserve, uint256 poolEmissionRate) = master.getPoolInfo(address(this));
    uint256 endOfEpochBlock = master.getEndOfEpochBlock(address(this)); // Assume this function exists or a similar mechanism to retrieve endOfEpochBlock

    // Ensure rewards are calculated within the epoch
    uint256 effectiveLastRewardBlock = lastRewardTime < endOfEpochBlock ? lastRewardTime : endOfEpochBlock;

    if ((reserve > 0 || _currentBlockTimestamp() > effectiveLastRewardBlock) && _lpSupplyWithMultiplier > 0) {
        uint256 duration = _currentBlockTimestamp().sub(effectiveLastRewardBlock);
        uint256 tokenRewards = duration.mul(poolEmissionRate).add(reserve);
        accRewardsPerShare = accRewardsPerShare.add(tokenRewards.mul(1e18).div(_lpSupplyWithMultiplier));
    }

    return position.amountWithMultiplier.mul(accRewardsPerShare).div(1e18).sub(position.rewardDebt)
        .add(position.pendingXPlaneRewards).add(position.pendingPlaneRewards);
}


```
