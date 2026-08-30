---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-H-2 hedgeDelta() priceToUse is calculated wrong, which causes bad hedges
vuln_class: []
---

# TRST-H-2 hedgeDelta() priceToUse is calculated wrong, which causes bad hedges

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
When _delta parameter is negative for `hedgeDelta()`, priceToUse will be the minimum 
between quotePrice and underlyingPrice. 
```solidity
    // buy wETH
    // lowest price is best price when buying
        uint256 priceToUse = quotePrice < underlyingPrice ? quotePrice : 
            underlyingPrice;
    RangeOrderDirection direction = inversed ? RangeOrderDirection.ABOVE 
        : RangeOrderDirection.BELOW;
    RangeOrderParams memory rangeOrder = 
        _getTicksAndMeanPriceFromWei(priceToUse, direction);
```
This works fine when direction is BELOW, because the calculated lowerTick and upperTick 
from _getTicksAndMeanPriceFromWei are guaranteed to be lower than current price.

```solidity
    int24 lowerTick = direction == RangeOrderDirection.ABOVE ? 
         nearestTick + tickSpacing : nearestTick - (2 * tickSpacing);
     int24 tickUpper = direction ==RangeOrderDirection.ABOVE ? lowerTick + 
        tickSpacing : nearestTick - tickSpacing;
```
Therefore, the fulfill condition is not true and we mint from the correct base. However, 
when direction is ABOVE, it is possible that the oracle supplied price (underlyingPrice) is low 
enough in comparison to pool price, that the fulfill condition is already active. In that case, 
the contract tries to mint from the wrong asset which will cause the wrong tokens to be sent 
in. In effect, the contract is not hedging.
A similar situation occurs when _delta parameter is greater than zero.

**Recommended Mitigation:**
Verify the calculated priceToUse is on the same side as pool-calculated tick price.

**Team Response:**
Fixed

**Mitigation review:**
The issue has been solved in the **_delta < 0** branch of **hedgeDelta()**, however it still exists in 
the else clause. Make sure to use the new **getPriceToUse()** utility in both cases.
