---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Misleading liquidity value returned when adding liquidity
vuln_class: []
---

# Misleading liquidity value returned when adding liquidity

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** When a user adds liquidity to a pool using either of the two hooks, the `addLiquidity()` function returns a value representing the amount of liquidity the user will receive in the `IncentivizedERC20` form; however, It can be seen in the below snippet that the returned value is the actual liquidity deposited to the pool:

```solidity
function addLiquidity(AddLiquidityParams calldata params)
    external
    payable
    nonReentrant
    ensure(params.deadline)
    returns (uint128 liquidity)
{
    ...
    liquidity = LiquidityAmounts.getLiquidityForAmounts(
        sqrtPriceX96,
        TickMath.getSqrtPriceAtTick(params.range.tickLower),
        TickMath.getSqrtPriceAtTick(params.range.tickUpper),
        params.amount0Desired,
        params.amount1Desired
    );

    if (rangeLiquidity == 0 && liquidity <= MINIMUM_LIQUIDITY) {
        revert LiquidityDoesntMeetMinimum();
    }
    // Add liquidity to the Pool
    BalanceDelta addedDelta = modifyLiquidity(
        params.key,
        params.range,
        IPoolManager.ModifyLiquidityParams({
            tickLower: params.range.tickLower,
            tickUpper: params.range.tickUpper,
            liquidityDelta: liquidity.toInt256(),
            salt: 0
        })
    );

    uint256 liquidityMinted;
    if (rangeLiquidity == 0) {
        // permanently lock the first MINIMUM_LIQUIDITY tokens
        liquidityMinted = liquidity - MINIMUM_LIQUIDITY;
        IncentivizedERC20(lpToken).mint(address(0), MINIMUM_LIQUIDITY);
        // Mint the LP tokens to the user
        IncentivizedERC20(lpToken).mint(params.to, liquidityMinted);
    } else {
        // Calculate the amount of LP tokens to mint
        (uint128 newRangeLiquidity,,) =
            poolManager.getPositionInfo(poolId, address(this), params.range.tickLower, params.range.tickUpper, 0);
        liquidityMinted =
            FullMath.mulDiv(IncentivizedERC20(lpToken).totalSupply(), liquidity, newRangeLiquidity - liquidity);
        // Mint the LP tokens to the user
        IncentivizedERC20(lpToken).mint(params.to, liquidityMinted);
    }

    ...
}
```

For the initial minimum liquidity deposit, an amount of `1e3` is subtracted to compute the actual amount of `IncentivizedERC20` tokens to mint, making this return value incorrect. Additionally, when the value of the `IncentivizedERC20` and the liquidity de-pegs, this function will return the actual liquidity deposited to the pool and not the amount minted.

```solidity
/// @return liquidity Amount of liquidity minted
```

Note that while the above NatSpec tag is present, this can be quite misleading because the correspondence between the actual amount of liquidity added to the Uniswap pool and `IncentivizedERC20` tokens minted in exchange is broken. Both users and external integrators are likely to reference this value when later removing liquidity, making this potentially problematic as attempting to remove liquidity with a returned value that is larger than the actual amount of tokens minted will revert.

**Impact:** The value returned when adding liquidity is misleading and does not accurately represent the `IncentivizedERC20` tokens minted. This could cause problems for user, integrators, and other off-chain indexing infrastructure.

**Proof of Concept:**
```solidity
function test_MisleadingReturnedLiquidityValue() public {
    initPool(key.currency0, key.currency1, IHooks(hookAddress), 3000, SQRT_PRICE_1_1);

    uint128 liquidity = fullRange.addLiquidity(
        FullRangeHook.AddLiquidityParams(
            key.currency0, key.currency1, 3000, 10e6, 10e6, 0, 0, address(this), MAX_DEADLINE
        )
    );

    (, address liquidityToken) = fullRange.poolInfo(id);

    IncentivizedERC20(liquidityToken).approve(address(fullRange), type(uint256).max);

    // The returned liquidity is used to remove but it fails due to misleading value
    FullRangeHook.RemoveLiquidityParams memory removeLiquidityParams =
        FullRangeHook.RemoveLiquidityParams(key.currency0, key.currency1, 3000, liquidity, MAX_DEADLINE);

    vm.expectRevert();
    fullRange.removeLiquidity(removeLiquidityParams);
}
```


**Recommended Mitigation:** Consider returning the `liquidityMinted` instead, since this is the actual value minted by the `IncentivizedERC20` token:

```diff
    function addLiquidity(AddLiquidityParams calldata params)
        external
        payable
        nonReentrant
        ensure(params.deadline)
--      returns (uint128 liquidity)
++      returns (uint128 liquidityMinted)
    {
        ...

        // Calculate the amount of liquidity to be added based on Currencies amounts
--      liquidity = LiquidityAmounts.getLiquidityForAmounts(
++      uint128 liquidity = LiquidityAmounts.getLiquidityForAmounts(
            sqrtPriceX96,
            TickMath.getSqrtPriceAtTick(MIN_TICK),
            TickMath.getSqrtPriceAtTick(MAX_TICK),
            params.amount0Desired,
            params.amount1Desired
        );

        ...

        // @gas cache pool's liquidity token
        IncentivizedERC20 poolLiquidityToken = IncentivizedERC20(poolInfo[poolId].liquidityToken);

--      uint256 liquidityMinted;
        if (poolLiquidity == 0) {
            // permanently lock the first MINIMUM_LIQUIDITY tokens
            liquidityMinted = liquidity - MINIMUM_LIQUIDITY;
            poolLiquidityToken.mint(address(0), MINIMUM_LIQUIDITY);
            // Mint the LP tokens to the user
            poolLiquidityToken.mint(params.to, liquidityMinted);
        } else {
            // Calculate the amount of LP tokens to mint
--          liquidityMinted = FullMath.mulDiv(
++          liquidityMinted = uint128(FullMath.mulDiv(
                poolLiquidityToken.totalSupply(),
                liquidity,
                poolManager.getLiquidity(poolId) - liquidity
--          );
++          ));
            // Mint the LP tokens to the user
            poolLiquidityToken.mint(params.to, liquidityMinted);
        }

        ...
    }
```

**Paladin:** Fixed by commit [`fd9d2c9`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/fd9d2c9f3bac0665483ab0c7ec1e5e62f1e731e6).

**Cyfrin:** Verified. The actual minted liquidity amount is now returned.
