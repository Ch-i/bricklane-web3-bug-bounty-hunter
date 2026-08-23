---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-L-4 _getUnderlyingBalances() does unnecessary computation when not in
  active position
vuln_class: []
---

# TRST-L-4 _getUnderlyingBalances() does unnecessary computation when not in active position

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
If the RangeOrderReactor contract is not currently active, it should simply return the current 
token balances. However, it does a lot of expensive logic to calculate position value.
```solidity
      (uint128 liquidity, uint256 feeGrowthInside0Last, uint256 feeGrowthInside1Last, uint128 tokensOwed0,
        uint128 tokensOwed1) = pool.positions(_getPositionID());
        // compute current holdings from liquidity
             (amount0Current, amount1Current) = 
        LiquidityAmounts.getAmountsForLiquidity(
        sqrtRatioX96,
        currentPosition.activeLowerTick.getSqrtRatioAtTick(),
             currentPosition.activeUpperTick.getSqrtRatioAtTick(),
        liquidity
        );
        // compute current fees earned
                    uint256 fee0 =
                _computeFeesEarned(true, feeGrowthInside0Last, tick, liquidity) +
            uint256(tokensOwed0);
        uint256 fee1 =
        _computeFeesEarned(false, feeGrowthInside1Last, tick, liquidity) 
        +
        uint256(tokensOwed1);
```

**Recommended mitigation:**
Perform early exit in case position is not active.

**Team response**
Fixed

**Mitigation Review**
Issue was addressed with correct early exit.
