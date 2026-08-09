---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-4-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: '`AngstromL2::_oneForZeroCreditRewards` should skip execution of range reward
  logic if there is no liquidity'
vuln_class: []
---

# `AngstromL2::_oneForZeroCreditRewards` should skip execution of range reward logic if there is no liquidity

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** When crediting top-of-block tax rewards, `AngstromL2::_zeroForOneCreditRewards` skips execution if there is no liquidity in the given range:

```solidity
if (tickNext >= lastTick && liquidity != 0) {
```

However, the equivalent condition within `AngstromL2::_oneForZeroCreditRewards` is implemented incorrectly:

```solidity
if (tickNext <= lastTick || liquidity == 0) {
```

This causes execution to continue into the range reward calculation logic even when there is no liquidity in the given range. This is effectively a no-op since:

* `delta0` and `delta1` will both be evaluated as `0`.
* `rangeReward` will thus also be assigned as `0`.
* `taxInEther` will remain unchanged.
* `cumulativeGrowthX128` will also remain unchanged, although this is almost accidental as `PoolRewardsLib::getGrowthDelta` will return zero when called with zero liquidity due to the behavior of `FixedPointMathLib::rawDiv`, narrowly avoiding a revert.

```solidity
    function getGrowthDelta(uint256 reward, uint256 liquidity)
        internal
        pure
        returns (uint256 growthDeltaX128)
    {
        if (!(reward < 1 << 128)) revert RewardOverflow();
@>      return (reward << 128).rawDiv(liquidity);
    }
```

Therefore, this logic should be skipped when there is no liquidity inside the range.

**Proof of Concept:** The following standalone file should be added to the test suite:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/console2.sol";
import {Pretty} from "./_helpers/Pretty.sol";
import {PoolRewards, PoolRewardsLib} from "../src/types/PoolRewards.sol";
import {CompensationPriceFinder} from "../src/libraries/CompensationPriceFinder.sol";
import {TickIteratorLib, TickIteratorUp} from "../src/libraries/TickIterator.sol";
import {SqrtPriceMath} from "v4-core/src/libraries/SqrtPriceMath.sol";
import {Q96MathLib} from "../src/libraries/Q96MathLib.sol";
import {FixedPointMathLib} from "solady/src/utils/FixedPointMathLib.sol";
import {MixedSignLib} from "../src/libraries/MixedSignLib.sol";
import {Slot0} from "v4-core/src/types/Slot0.sol";

import {BaseTest} from "./_helpers/BaseTest.sol";
import {RouterActor} from "./_mocks/RouterActor.sol";
import {MockERC20} from "super-sol/mocks/MockERC20.sol";
import {UniV4Inspector} from "./_mocks/UniV4Inspector.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolId, PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {BalanceDelta} from "v4-core/src/types/BalanceDelta.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {LPFeeLibrary} from "v4-core/src/libraries/LPFeeLibrary.sol";

import {AngstromL2} from "../src/AngstromL2.sol";
import {getRequiredHookPermissions, POOLS_MUST_HAVE_DYNAMIC_FEE} from "../src/hook-config.sol";
import {IUniV4} from "../src/interfaces/IUniV4.sol";

import {IFlashBlockNumber} from "src/interfaces/IFlashBlockNumber.sol";

contract AngstromL2RewardsTest is BaseTest {

    using PoolIdLibrary for PoolKey;
    using IUniV4 for UniV4Inspector;
    using IUniV4 for IPoolManager;
    using TickMath for int24;
    using Q96MathLib for uint256;
    using FixedPointMathLib for *;
    using MixedSignLib for *;

    using Pretty for *;

    UniV4Inspector manager;
    RouterActor router;
    AngstromL2 angstrom;

    MockERC20 token;

    uint160 constant INIT_SQRT_PRICE = 1 << 96; // 1:1 price
    int24[2][] positionRanges; // Track positions ranges added with addLiquidity helper
    mapping(PoolId id => PoolRewards) internal rewardsModified;
    mapping(PoolId id => PoolRewards) internal rewardsOriginal;

    function setUp() public {
        vm.roll(100);
        manager = new UniV4Inspector();
        router = new RouterActor(manager);
        vm.deal(address(router), 100 ether);

        token = new MockERC20();
        token.mint(address(router), 1_000_000_000e18);

        angstrom = AngstromL2(
            deployAngstromL2(
                type(AngstromL2).creationCode,
                IPoolManager(address(manager)),
                address(this),
                getRequiredHookPermissions(),
                IFlashBlockNumber(address(0))
            )
        );
    }

    function initializePool(address asset1, int24 tickSpacing, int24 startTick)
        internal
        returns (PoolKey memory key)
    {
        require(asset1 != address(0), "Token cannot be address(0)");

        key = PoolKey({
            currency0: Currency.wrap(address(0)),
            currency1: Currency.wrap(asset1),
            fee: POOLS_MUST_HAVE_DYNAMIC_FEE ? LPFeeLibrary.DYNAMIC_FEE_FLAG : 0,
            tickSpacing: tickSpacing,
            hooks: IHooks(address(angstrom))
        });

        manager.initialize(key, TickMath.getSqrtPriceAtTick(startTick));

        return key;
    }

    /// @notice Helper to add liquidity on a given tick range
    /// @param key The pool key
    /// @param tickLower The lower tick of the range
    /// @param tickUpper The upper tick of the range
    /// @param liquidityAmount The amount of liquidity to add
    function addLiquidity(
        PoolKey memory key,
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidityAmount
    ) internal returns (BalanceDelta delta) {
        require(tickLower % key.tickSpacing == 0, "Lower tick not aligned");
        require(tickUpper % key.tickSpacing == 0, "Upper tick not aligned");
        require(tickLower < tickUpper, "Invalid tick range");

        (delta,) = router.modifyLiquidity(
            key, tickLower, tickUpper, int256(uint256(liquidityAmount)), bytes32(0)
        );

        // console.log("delta.amount0(): %s", delta.amount0().fmtD());
        // console.log("delta.amount1(): %s", delta.amount1().fmtD());
        positionRanges.push([tickLower, tickUpper]);

        return delta;
    }

    /*
     *  Shows that this doesn't revert even though it crosses through
     *  a range of zero liquidity
     */
    function test_cyfrin_TestOneForZeroOnZeroLiquidityRange() public {
        PoolKey memory key = initializePool(address(token), 10, 3);

        setPriorityFee(100 gwei);
        addLiquidity(key, 0,  10, 1e22);
        /* Leave a gap of zero liquidity */
        addLiquidity(key, 20, 30, 1e22);
        router.swap(key, false, 1000e18, int24(25).getSqrtPriceAtTick());
        logRewards("after", key);
    }

    function test_cyfrin_PoolRewardsGetGrowthDeltaDoesntRevertOnZeroLiqudity() public {
        PoolRewardsLib.getGrowthDelta(0,0);
    }

    error RewardOverflow();

    /// forge-config: default.allow_internal_expect_revert = true
    function test_cyfrin_GetGrowthDeltaWouldRevertWithoutRawDiv() public {
         vm.expectRevert();
        _getGrowthDelta(0,0);
    }

    function test_cyfrin_OneForZeroCreditRewardsWorksWithModifiedLogic() public {
        uint128 LIQUIDITY = 1e22;
        uint256 PRIORITY_FEE = 100 gwei;
        int24[4] memory TICKS_TO_CHECK = [int24(0), 10, 20, 30];


        PoolKey memory key = initializePool(address(token), 10, 3);
        PoolId id = key.toId();

        setPriorityFee(PRIORITY_FEE);
        addLiquidity(key, 0,  10, LIQUIDITY);
        /* Leave a gap of zero liquidity */
        addLiquidity(key, 20, 30, LIQUIDITY);

        Slot0 slot0BeforeSwap = manager.getSlot0(id);
        router.swap(key, false, 1000e18, int24(25).getSqrtPriceAtTick());
        Slot0 slot0AfterSwap = manager.getSlot0(id);

        TickIteratorUp memory ticks = TickIteratorLib.initUp(
            IPoolManager(manager), id, 10, slot0BeforeSwap.tick(), slot0AfterSwap.tick()
        );

        uint256 taxInEther = angstrom.getSwapTaxAmount(PRIORITY_FEE);

        (int24 lastTick, uint160 pstarSqrtX96) = CompensationPriceFinder.getOneForZero(
            ticks, LIQUIDITY, taxInEther, slot0BeforeSwap, slot0AfterSwap
        );

        _oneForZeroCreditRewardsModified(ticks,1e22,taxInEther,slot0BeforeSwap.sqrtPriceX96(),lastTick,pstarSqrtX96);
        _oneForZeroCreditRewardsOriginal(ticks,1e22,taxInEther,slot0BeforeSwap.sqrtPriceX96(),lastTick,pstarSqrtX96);

        assertEq(rewardsOriginal[id].globalGrowthX128, rewardsModified[id].globalGrowthX128);


        for (uint256 i = 0; i < TICKS_TO_CHECK.length; i++) {
            int24 tick = TICKS_TO_CHECK[i];
            assertEq(rewardsOriginal[id].rewardGrowthOutsideX128[tick],
                     rewardsModified[id].rewardGrowthOutsideX128[tick]);
        }

    }


    /*********************************************************************/

    /*
     * Logic copied from PoolRewardsLib.getGrowthDelta and modified to not use `rawDiv`
     */
    function _getGrowthDelta(uint256 reward, uint256 liquidity)
        internal
        pure
        returns (uint256 growthDelta)
    {
        if (!(reward < 1 << 128)) revert RewardOverflow();
        return (reward << 128) / (liquidity);
    }

    function _min(uint160 x, uint160 y) internal pure returns (uint160) {
        return x < y ? x : y;
    }

    /*
     * Logic copied from AngstromL2.sol and modified to have following if-condition:
     *
     *    if (tickNext <= lastTick && liquidity != 0) {
     *
     * Also code modifies `rewardsModified` instead of `rewards` mapping
     */
    function _oneForZeroCreditRewardsModified(
        TickIteratorUp memory ticks,
        uint128 liquidity,
        uint256 taxInEther,
        uint160 priceLowerSqrtX96,
        int24 lastTick,
        uint160 pstarSqrtX96
    ) internal {
        uint256 pstarX96 = uint256(pstarSqrtX96).mulX96(pstarSqrtX96);
        uint256 cumulativeGrowthX128 = 0;
        uint160 priceUpperSqrtX96;

        while (ticks.hasNext()) {
            int24 tickNext = ticks.getNext();

            priceUpperSqrtX96 = _min(TickMath.getSqrtPriceAtTick(tickNext), pstarSqrtX96);

            uint256 rangeReward = 0;
            if (tickNext <= lastTick && liquidity != 0) {
                uint256 delta0 = SqrtPriceMath.getAmount0Delta(
                    priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false
                );
                uint256 delta1 = SqrtPriceMath.getAmount1Delta(
                    priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false
                );
                rangeReward = (delta0 - delta1.divX96(pstarX96)).min(taxInEther);

                unchecked {
                    taxInEther -= rangeReward;
                    cumulativeGrowthX128 += PoolRewardsLib.getGrowthDelta(rangeReward, liquidity);
                }
            }

            unchecked {
                rewardsModified[ticks.poolId].rewardGrowthOutsideX128[tickNext] += cumulativeGrowthX128;
            }

            (, int128 liquidityNet) = ticks.manager.getTickLiquidity(ticks.poolId, tickNext);
            liquidity = liquidity.add(liquidityNet);

            priceLowerSqrtX96 = priceUpperSqrtX96;
        }

        // Distribute remainder to last range and update global accumulator.
        unchecked {
            cumulativeGrowthX128 += PoolRewardsLib.getGrowthDelta(taxInEther, liquidity);
            rewardsModified[ticks.poolId].globalGrowthX128 += cumulativeGrowthX128;
        }
    }

    /*
     * Original logic for _oneForZeroCreditRewards but modifying `rewardsOriginal` instead of `rewards` mapping
     */

    function _oneForZeroCreditRewardsOriginal(
        TickIteratorUp memory ticks,
        uint128 liquidity,
        uint256 taxInEther,
        uint160 priceLowerSqrtX96,
        int24 lastTick,
        uint160 pstarSqrtX96
    ) internal {
        uint256 pstarX96 = uint256(pstarSqrtX96).mulX96(pstarSqrtX96);
        uint256 cumulativeGrowthX128 = 0;
        uint160 priceUpperSqrtX96;

        while (ticks.hasNext()) {
            int24 tickNext = ticks.getNext();

            priceUpperSqrtX96 = _min(TickMath.getSqrtPriceAtTick(tickNext), pstarSqrtX96);

            uint256 rangeReward = 0;
            if (tickNext <= lastTick || liquidity == 0) {
                uint256 delta0 = SqrtPriceMath.getAmount0Delta(
                    priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false
                );
                uint256 delta1 = SqrtPriceMath.getAmount1Delta(
                    priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false
                );
                rangeReward = (delta0 - delta1.divX96(pstarX96)).min(taxInEther);

                unchecked {
                    taxInEther -= rangeReward;
                    cumulativeGrowthX128 += PoolRewardsLib.getGrowthDelta(rangeReward, liquidity);
                }
            }

            unchecked {
                rewardsOriginal[ticks.poolId].rewardGrowthOutsideX128[tickNext] += cumulativeGrowthX128;
            }

            (, int128 liquidityNet) = ticks.manager.getTickLiquidity(ticks.poolId, tickNext);
            liquidity = liquidity.add(liquidityNet);

            priceLowerSqrtX96 = priceUpperSqrtX96;
        }

        // Distribute remainder to last range and update global accumulator.
        unchecked {
            cumulativeGrowthX128 += PoolRewardsLib.getGrowthDelta(taxInEther, liquidity);
            rewardsOriginal[ticks.poolId].globalGrowthX128 += cumulativeGrowthX128;
        }
    }



    /*
     * Helper functions
     */

    function logRewards(string memory s, PoolKey memory key) internal {
        bytes32 SALT = bytes32(0);
        console2.log("Rewards %s {", s);
        for (uint256 i = 0; i < positionRanges.length; i++) {

            int24 lower = positionRanges[i][0];
            int24 upper = positionRanges[i][1];

            uint256 rewards = angstrom.getPendingPositionRewards(key, address(router), lower, upper, SALT);
            console2.log("  rewards in [%s,%s]: %s", vm.toString(lower), vm.toString(upper), rewards.pretty());
        }
        console2.log("}");
    }
}
```

**Recommended Mitigation:** Modify the condition within `AngstromL2::_oneForZeroCreditRewards` to:

```solidity
if (tickNext <= lastTick && liquidity != 0)
```

**Sorella Labs:** Fixed in commit [d53cc19](https://github.com/SorellaLabs/l2-angstrom/commit/d53cc197c43fc2d1db6d946def3fe847c2e1281c).

**Cyfrin:** Verified.
