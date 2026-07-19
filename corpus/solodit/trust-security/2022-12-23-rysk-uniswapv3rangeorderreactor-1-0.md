---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-M-1 multiplication overflow in getPoolPrice() likely
vuln_class: []
---

# TRST-M-1 multiplication overflow in getPoolPrice() likely

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
`getPoolPrice()` is used in hedgeDelta to get the price directly from Uniswap v3 pool:
```solidity 
    function getPoolPrice() public view returns (uint256 price, uint256 
         inversed){
            (uint160 sqrtPriceX96, , , , , , ) = pool.slot0();
        uint256 p = uint256(sqrtPriceX96) * uint256(sqrtPriceX96) * (10 
        ** token0.decimals());
     // token0/token1 in 1e18 format
          price = p / (2 ** 192);
              inversed = 1e36 / price;
         }

```
The issue is that calculation of p is likely to overflow. sqrtPriceX96 has 96 bits for decimals, 
10** `token0.decimals()` will have 60 bits when decimals is 18, therefore there is only 
(256 – 2 * 96 – 60) / 2 = 2 bits for non-decimal part of sqrtPriceX96. 

**Recommended Mitigation:**
Consider converting the sqrtPrice to a 60x18 format and performing arithmetic operations 
using the PRBMathUD60x18 library.

**Team Response:**
Fixed

**Mitigation Review**
Calculations are now performed safely using the standard FullMath library
