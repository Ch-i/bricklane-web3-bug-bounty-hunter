---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Missing tick validation when creating a new range in `MultiRangeHook`
vuln_class: []
---

# Missing tick validation when creating a new range in `MultiRangeHook`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** When adding liquidity to a pool configured with the `MultiRangeHook`, it is necessary to first initialize the pool and create the desired range. Users are limited to adding liquidity to tick ranges that are multiples of the configured `tickSpacing` of the pool, such that an attempt to add liquidity in the range `[-50, 50]` for a pool configured with a tick spacing of `60` will fail. This is due to a revert with `TickMisaligned()` originating from `TickBitmap::flipTick` invoked within `Pool::modifyLiquidity`. However, `MultiRangeHook::createRange` does not currently perform any validation on the tick range. It is therefore possible to create an invalid range that will create an unusable `IncentivizedERC20` token, wasting the caller's gas.

**Impact:** Ranges that cannot be used can be created within `MultiRangeHook` and pushed to the `poolLpTokens` array.

**Proof of Concept:**
```solidity
function test_InvalidTickRangeCreation() public {
    int24 lowerTick = -90;
    int24 upperTick = 90;

    // Pool with 20 tick spacing
    initPool(key2.currency0, key2.currency1, IHooks(address(multiRange)), 1000, SQRT_PRICE_1_1);

    rangeKey = RangeKey(id2, lowerTick, upperTick);
    rangeId = rangeKey.toId();

    multiRange.createRange(key2, rangeKey);

    uint256 token0Amount = 100 ether;
    uint256 token1Amount = 100 ether;

    vm.expectRevert(abi.encodeWithSelector(TickBitmap.TickMisaligned.selector, lowerTick, int256(int24(20))));
    multiRange.addLiquidity(
        MultiRangeHook.AddLiquidityParams(
            key2, rangeKey, token0Amount, token1Amount, 99 ether, 99 ether, address(this), MAX_DEADLINE
        )
    );
}
```


**Recommended Mitigation:** Validate the newly-created range against the pool tick spacing to ensure there is no mismatch:
```diff
    function createRange(PoolKey calldata key, RangeKey calldata rangeKey) external {
++      if(
++          rangeKey.tickLower % key.tickSpacing != 0 ||
++          rangeKey.tickUpper % key.tickSpacing != 0
++      ) revert();


        PoolId poolId = key.toId();
        RangeId rangeId = rangeKey.toId();

        if (!initializedPools[poolId]) revert PoolNotInitialized();
        if (alreadyCreatedRanges[poolId][rangeId] || rangeLpToken[rangeId] != address(0)) revert RangeAlreadyCreated();
        alreadyCreatedRanges[poolId][rangeId] = true;

        ...
    }
```

**Paladin:** Fixed by commit [`0db4aea`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/0db4aea4eda83d3ddf3a655280474f7731866161).

**Cyfrin:** Verified. The range ticks are now validated against the tick spacing.
