---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-15
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Rewards distribution DoS due to uncached secondary asset classes
vuln_class: []
---

# Rewards distribution DoS due to uncached secondary asset classes

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The rewards calculation directly accesses the totalStakeCache mapping instead of using the getTotalStake() function with proper fallback logic:

```solidity
function _calculateOperatorShare(uint48 epoch, address operator) internal {
  // code..

  uint96[] memory assetClasses = l1Middleware.getAssetClassIds();
  for (uint256 i = 0; i < assetClasses.length; i++) {
       uint256 totalStake = l1Middleware.totalStakeCache(epoch, assetClasses[i]); //@audit directly accesses totalStakeCache
  }
}
```
Only specific operations trigger caching for secondary asset classes:
```solidity
// @audit following only cache PRIMARY_ASSET_CLASS (asset class 1)
addNode(...) updateStakeCache(getCurrentEpoch(), PRIMARY_ASSET_CLASS)
forceUpdateNodes(...) updateStakeCache(getCurrentEpoch(), PRIMARY_ASSET_CLASS)

// @audit only caches the specific asset class being slashed
slash(epoch, operator, amount, assetClassId) updateStakeCache(epoch, assetClassId)
```
Secondary asset classes (2, 3, etc.) are only cached when:

- Slashing occurs for that specific asset class (infrequent)
- Manual calcAndCacheStakes() calls (requires intervention)

As a result, when rewards distributor calls `distributeRewards`, for the specific asset class ID with uncached stake, `_calculateOperatorShare` leads to a division by zero error.

**Impact:** Rewards distribution fails for affected epochs. It is worthwhile to note that DoS is temporary - manual intervention by calling `calcAndCacheStakes` for specific asset class ID's can fix the DoS error.

**Proof of Concept:** Add the following test to `RewardsTest.t.sol`

```solidity
function test_RewardsDistributionDOS_With_UncachedSecondaryAssetClasses() public {
    uint48 epoch = 1;
    uint256 uptime = 4 hours;

    // Setup stakes for operators normally
    _setupStakes(epoch, uptime);

    // Set totalStakeCache to 0 for secondary asset classes to simulate uncached state
    middleware.setTotalStakeCache(epoch, 2, 0); // Secondary asset class 2
    middleware.setTotalStakeCache(epoch, 3, 0); // Secondary asset class 3

    // Keep primary asset class cached (this would be cached by addNode/forceUpdateNodes)
    middleware.setTotalStakeCache(epoch, 1, 100000); // This stays cached


    // Move to epoch where distribution is allowed (must be at least 2 epochs ahead)
    vm.warp((epoch + 3) * middleware.EPOCH_DURATION());

    // Attempt to distribute rewards - this should fail due to division by zero
    // when _calculateOperatorShare tries to calculate rewards for uncached secondary asset classes
    vm.expectRevert(); // This should revert due to division by zero in share calculation

    vm.prank(REWARDS_DISTRIBUTOR_ROLE);
    rewards.distributeRewards(epoch, 3);
}

```

**Recommended Mitigation:** Consider checking and caching stake for assetIds if it doesn't exist.

```diff solidity
function _calculateOperatorShare(uint48 epoch, address operator) internal {
  // code..

  uint96[] memory assetClasses = l1Middleware.getAssetClassIds();
  for (uint256 i = 0; i < assetClasses.length; i++) {
++       uint256 totalStake = l1Middleware.totalStakeCache(epoch, assetClasses[i]);
++       if (totalStake == 0) {
++            l1Middleware.calcAndCacheStakes(epoch, assetClasses[i]);
++             totalStake = l1Middleware.totalStakeCache(epoch, assetClasses[i]);
++       }
       // code
  }
}
```

**Suzaku:**
Fixed in commit [f76d1f4](https://github.com/suzaku-network/suzaku-core/pull/155/commits/f76d1f44208e9e882047713a8c49d16cccc69e36).

**Cyfrin:** Verified.
