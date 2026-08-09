---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-5-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Unnecessary liquidity read and subtraction operation can be removed
vuln_class: []
---

# Unnecessary liquidity read and subtraction operation can be removed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** `FullRangeHook::addLiquidity` works as follows:
```solidity
function addLiquidity(AddLiquidityParams calldata params)
    external
    payable
    nonReentrant
    ensure(params.deadline)
    returns (uint128 liquidity)
{
    ...
    // Read the pool liquidity previous to the addition
    uint128 poolLiquidity = poolManager.getLiquidity(poolId);

    // Calculate the amount of liquidity to be added to the pool
    liquidity = LiquidityAmounts.getLiquidityForAmounts(
        sqrtPriceX96,
        TickMath.getSqrtPriceAtTick(MIN_TICK),
        TickMath.getSqrtPriceAtTick(MAX_TICK),
        params.amount0Desired,
        params.amount1Desired
    );

    if (poolLiquidity == 0 && liquidity <= MINIMUM_LIQUIDITY) {
        revert LiquidityDoesntMeetMinimum();
    }
    // Add the liquidity to the pool
    BalanceDelta addedDelta = modifyLiquidity(
        key,
        IPoolManager.ModifyLiquidityParams({
            tickLower: MIN_TICK,
            tickUpper: MAX_TICK,
            liquidityDelta: liquidity.toInt256(),
            salt: 0
        })
    );

    // @gas cache pool's liquidity token
    IncentivizedERC20 poolLiquidityToken = IncentivizedERC20(poolInfo[poolId].liquidityToken);

    uint256 liquidityMinted;
    if (poolLiquidity == 0) {
        ...
    } else {
        // Calculate the amount of LP tokens to mint
@>      liquidityMinted = FullMath.mulDiv(
            poolLiquidityToken.totalSupply(),
            liquidity,
            poolManager.getLiquidity(poolId) - liquidity
        );
        // Mint the LP tokens to the user
        poolLiquidityToken.mint(params.to, liquidityMinted);
    }
    ...
}
```

The final computation of the liquidity minted is the total LP token supply, multiplied by the added liquidity and divided by the previous liquidity. The previous liquidity is computed by fetching the current pool liquidity and subtracting the added liquidity; however, these two operations are redundant as the result will always be the same as the previously fetched `poolLiquidity` which is the liquidity from the pool before the addition.

**Recommended Mitigation:**
```diff
    function addLiquidity(AddLiquidityParams calldata params)
        external
        payable
        nonReentrant
        ensure(params.deadline)
        returns (uint128 liquidity)
    {
        ...
        uint128 poolLiquidity = poolManager.getLiquidity(poolId);
        ...
        uint256 liquidityMinted;
        if (poolLiquidity == 0) {
            // permanently lock the first MINIMUM_LIQUIDITY tokens
            liquidityMinted = liquidity - MINIMUM_LIQUIDITY;
            poolLiquidityToken.mint(address(0), MINIMUM_LIQUIDITY);
            // Mint the LP tokens to the user
            poolLiquidityToken.mint(params.to, liquidityMinted);
        } else {
            // Calculate the amount of LP tokens to mint
            liquidityMinted = FullMath.mulDiv(
                poolLiquidityToken.totalSupply(),
                liquidity,
--              poolManager.getLiquidity(poolId) - liquidity
++              poolLiquidity
            );
            // Mint the LP tokens to the user
            poolLiquidityToken.mint(params.to, liquidityMinted);
        }
        ...
    }
```

**Paladin:** Fixed by commit [`d9450d1`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/d9450d1c830188ebd0dfc73f190fd2a8b4da2755).

**Cyfrin:** Verified. The cached value is now used.
