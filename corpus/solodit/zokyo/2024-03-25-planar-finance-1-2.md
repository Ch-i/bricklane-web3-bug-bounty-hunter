---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Lack of Minimum Waiting Period for `pendingRewards` Function Calls in `LpNFTPool`
  Contract
vuln_class: []
---

# Lack of Minimum Waiting Period for `pendingRewards` Function Calls in `LpNFTPool` Contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved

**Source**: LpNFTPool.sol , HyperPool.sol


**Description**:

The `pendingRewards` function in the `LpNFTPool` contract calculates the pending rewards for a staking position based on the current block timestamp and the last reward time. However, it lacks a mechanism to enforce a minimum waiting period between successive calls. This could potentially allow users to call this function excessively without any temporal restrictions

**Recommendation**:

To mitigate this issue, it is recommended to introduce a minimum waiting period for calling the `pendingRewards` function. This can be achieved by maintaining a mapping to track the last time the `pendingRewards` function was called for each `tokenId` and requiring that a certain amount of time (e.g., one hour) has passed before the function can be called again for the same `tokenId`. This approach ensures that there is a controlled frequency of reward calculations, 


```solidity
// SPDX-License-Identifier: MIT
pragma solidity =0.7.6;

// Import statements...

contract LpNFTPool is ReentrancyGuard, ILpNFTPool, ERC721("Planar Locked Position NFT", "lpNFT"), Blast {
  // Existing variable and function declarations...

  mapping(uint256 => uint256) private lastRewardCalculationTime; // Tracks the last time rewards were calculated for each tokenId
  uint256 private constant SECONDS_PER_HOUR = 3600; // Define the minimum waiting period

  // Existing constructor and function definitions...

  /**
   * @dev Returns pending rewards for a position with a minimum waiting period enforcement
   */
  function pendingRewards(uint256 tokenId) external view returns (uint256) {
    require(_currentBlockTimestamp() > lastRewardCalculationTime[tokenId] + SECONDS_PER_HOUR, "Wait for the minimum period before recalculating");

    StakingPosition storage position = _stakingPositions[tokenId];
    uint256 accRewardsPerShare = _accRewardsPerShare;
    (,,uint256 lastRewardTime, uint256 reserve, uint256 poolEmissionRate) = master.getPoolInfo(address(this));

    // Existing logic to recompute accRewardsPerShare if not up to date...

    return position.amountWithMultiplier.mul(accRewardsPerShare).div(1e18).sub(position.rewardDebt)
      .add(position.pendingXPlaneRewards).add(position.pendingPlaneRewards);
  }

  // Additional or modified functions as necessary...
}


```
