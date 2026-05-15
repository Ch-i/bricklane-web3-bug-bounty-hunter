---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: '`rewardGrowthOutsideX128` is not correctly initialized in `PoolRewards::updateAfterLiquidityAdd`'
vuln_class: []
---

# `rewardGrowthOutsideX128` is not correctly initialized in `PoolRewards::updateAfterLiquidityAdd`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** The Uniswap V3/V4 convention is that if a tick has just been initialized, and the current tick is to the right of that tick, then its `feeGrowthOutside[0/1]X1278` values must be initialized with `feeGrowthGlobal[0/1]X128`.

`PoolRewards::updateAfterLiquidityAdd` intends to replicate this logic and initialize the `rewardGrowthOutsideX128` for the relevant ticks; however, this function is called as part of the `AngstromL2::afterAddLiquidity` hook, at which point the ticks are initialized as the liquidity is non-zero. Thus e.g. `!pm.isInitialized(...)` will always return `false` and hence the body of the if-statement will never be executed, meaning this state is never initialized.

Fortunately, the presence of `lastGrowthInsideX128` corrects for what would otherwise be an overflow vector, mitigating for any potential impact. In the following analysis, let values be taken modulo 1000 for simplicity, i.e., within the range `[0, 999]` with wraparound at 1000.

Abbreviations:
- `gi` is `growthInsideX128`
- `lgi` is `lastGrowthInsideX128`
- `rgo` is `rewardsGrowthOutsideX128`
- `t` is current tick
- `G` is `globalGrowthX128`

Assume:
- `G == 10`
- `rgo[0] == 3`
- `rgo[10]` uninitialized
- `t = 11`

Now add some liquidity in `[0,10]`
`lgi = 0 - 3 = 997`

Consider the following three cases for `t`, assuming no new rewards were added.

**Case 1**: t has not moved
```
  gi - lgi
= rgo[10] - rgo[0] - lgi
= 0 - 3 - 997 = 997 - 997 = 0
```

**Case 2**: 0 <= t < 10
- `rgo[10]` flipped from 0 to 10 as `t` moved left

```
    gi - lgi
== G - rgo[0] - rgo[10] - lgi
== 10 - 3 - 10 - 997
== 997 - 997
== 0
```

**Case 3**: t < 0
Now `rgo[0]` flipped to `7 == 10 - 3` as `t` moved left

```
    gi - lgi
== rgo[0] - rgo[10] - lgi
== 7 - 10 - 997
== 997 - 997
== 0
```

Now reconsider the final two cases when rewards _do_ grow.

**Case 2**: `0 <= t < 10`.
- `G` grew by 2 to `12`
- `rgo[10]` grew by `1` (after flipping) to `11`

```
    gi - lgi
== 12 - 3 - 11 - 997
== 998 - 997
== 1
```

**Case 3**:  `t < 0`
- `G` grew by 3 to `13` (combination of rgo[10] and rgo[0] growth below)
- `rgo[10]` grew by 2 to `12`.
- `rgo[0]` grew by a further 1 (after flipping). `rgo[0] = 7 + 2 + 1 == 10`

```
    gi - lgi
== 10 - 12 - 997
== 998 - 997
== 1
```

This demonstrates that it is the cumulative growth of rewards outside that protects this logic from underflow.

**Proof of Concept:** The following test, which should be added to `AngstromL2.t.sol`, demonstrates how `rewardGrowthOutsideX128` is not correctly initialized:

```solidity
function test_cyfrin_IncorrectGrowthOutsideInitialization() public {
    uint256 PRIORITY_FEE = 0.7 gwei;
    PoolKey memory key = initializePool(address(token), 10, 7);

    angstrom.setPoolLPFee(key, 0.0005e6);
    addLiquidity(key, 0, 30, 10e21);
    bumpBlock();

    setPriorityFee(PRIORITY_FEE);

    // swap left and right to build up feeGrowthGlobal in both currencies
    router.swap(key, true,  -1000e18, int24(1).getSqrtPriceAtTick());
    bumpBlock();
    router.swap(key, false, -1000e18, int24(25).getSqrtPriceAtTick());

    setPriorityFee(0);
    bumpBlock();
    int24 tickLower = 10;
    int24 tickUpper = 20;
    addLiquidity(key, tickLower, tickUpper, 10e21);

    PoolId id = key.toId();

    // lower tick
    {
        (uint256 lowerFeeGrowthOutside0X128, uint256 lowerFeeGrowthOutside1X128) = StateLibrary.getTickFeeGrowthOutside(manager, id, tickLower);
        (uint256 lowerFeeGrowthGlobal0X128, uint256 lowerFeeGrowthGlobal1X128) = StateLibrary.getFeeGrowthGlobals(manager, id);
        uint256 lowerRewardGlobalGrowthX128 = angstrom.getRewardGlobalGrowthX128(id);
        uint256 lowerRewardGrowthOutsideX128 = angstrom.getRewardGrowthOutsideX128(id, tickLower);
        assertGt(lowerFeeGrowthGlobal0X128, 0);
        assertGt(lowerFeeGrowthGlobal1X128, 0);
        assertEq(lowerFeeGrowthOutside0X128, lowerFeeGrowthGlobal0X128);
        assertEq(lowerFeeGrowthOutside1X128, lowerFeeGrowthGlobal1X128);
        assertGt(lowerRewardGlobalGrowthX128, 0);
        /* BUG: lowerRewardGrowthOutsideX128 should be non-zero since lowerRewardGlobalGrowthX128 is non-zero! */
        assertEq(lowerRewardGrowthOutsideX128, 0);
    }

    // upper tick
    {
        (uint256 upperFeeGrowthOutside0X128, uint256 upperFeeGrowthOutside1X128) = StateLibrary.getTickFeeGrowthOutside(manager, id, tickUpper);
        (uint256 upperFeeGrowthGlobal0X128, uint256 upperFeeGrowthGlobal1X128) = StateLibrary.getFeeGrowthGlobals(manager, id);
        uint256 upperRewardGlobalGrowthX128 = angstrom.getRewardGlobalGrowthX128(id);
        uint256 upperRewardGrowthOutsideX128 = angstrom.getRewardGrowthOutsideX128(id, tickUpper);
        assertGt(upperFeeGrowthGlobal0X128, 0);
        assertGt(upperFeeGrowthGlobal1X128, 0);
        assertEq(upperFeeGrowthOutside0X128, upperFeeGrowthGlobal0X128);
        assertEq(upperFeeGrowthOutside1X128, upperFeeGrowthGlobal1X128);
        assertGt(upperRewardGlobalGrowthX128, 0);
        /* BUG: upperRewardGrowthOutsideX128 should be non-zero since upperRewardGlobalGrowthX128 is non-zero! */
        assertEq(upperRewardGrowthOutsideX128, 0);
    }
}
```

To successfully compile, first include the following import statements:

```solidity
import {StateLibrary} from "v4-core/src/libraries/StateLibrary.sol";
import {Position} from "../src/types/PoolRewards.sol";
```

Next, include the following test harness:

```solidity
contract AngstromL2Harness is AngstromL2 {
    constructor(IPoolManager uniV4, address owner, IFlashBlockNumber flashBlockNumberProvider)
        AngstromL2(uniV4, owner, flashBlockNumberProvider)
    {}

    function getRewardGrowthOutsideX128(PoolId id, int24 tick) public returns (uint256) {
        return rewards[id].rewardGrowthOutsideX128[tick];
    }

    function getRewardLastGrowthInsideX128(PoolId id, address owner, int24 tickLower, int24 tickUpper, bytes32 salt) public returns (uint256) {
        (Position storage pos, ) = rewards[id].getPosition(owner, tickLower, tickUpper, salt);
        return pos.lastGrowthInsideX128;
    }

    function getRewardGlobalGrowthX128(PoolId id) public returns (uint256) {
        return rewards[id].globalGrowthX128;
    }
}
```

And finally update the setup accordingly:

```solidity
AngstromL2Harness angstrom;
...
angstrom = AngstromL2Harness(
    deployAngstromL2(
        type(AngstromL2Harness).creationCode,
        IPoolManager(address(manager)),
        address(this),
        getRequiredHookPermissions(),
        IFlashBlockNumber(address(0))
    )
);
```

**Recommended Mitigation:** Implement the `beforeAddLiquidity()` hook and corresponding permission to call `PoolRewards::updateAfterLiquidityAdd` prior to adding liquidity.

**Sorella Labs:** Fixed in commit [cd0ac3c](https://github.com/SorellaLabs/l2-angstrom/commit/cd0ac3c1e8ad9ac1fc80820cb130b981429ca13d).

**Cyfrin:** Verified. The Uniswap initialization convention has been removed entirely to simplify the accumulator logic.

\clearpage
