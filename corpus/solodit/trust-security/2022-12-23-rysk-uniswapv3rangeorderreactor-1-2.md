---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-M-3 Overflow danger in _sqrtPriceX96ToUint
vuln_class: []
---

# TRST-M-3 Overflow danger in _sqrtPriceX96ToUint

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
_sqrtPriceX96ToUint will only work when the non-fractional component of sqrtPriceX96 
takes up to 32 bits. This represents a price ratio of 18446744073709551616. With different 
token digits it is not unlikely that this ratio will be crossed which will make hedgeDelta() 
revert.

    
```solidity
    function _sqrtPriceX96ToUint(uint160 sqrtPriceX96) private pure returns (uint256)
    {
        uint256 numerator1 = uint256(sqrtPriceX96) * 
         uint256(sqrtPriceX96);
    return FullMath.mulDiv(numerator1, 1, 1 << 192);
         }
```

**Recommended Mitigation:**
Perform the multiplication after converting the numbers to 60x18 variables

**Team Response:**
Fixed

**Mitigation review:**
New utility function sqrtPriceX96ToUint correctly uses SafeMath, and also multiplies in a 
different order depending on price size to ensure no overflows occur:

```solidity
        if (sqrtPrice > Q96) {
             uint256 sqrtP = FullMath.mulDiv(sqrtPrice, 10 ** token0Decimals, 
                Q96);
        return FullMath.mulDiv(sqrtP, sqrtP, 10 ** token0Decimals);
            } else {
        uint256 numerator1 = FullMath.mulDiv(sqrtPrice, sqrtPrice, 1);
        uint256 numerator2 = 10 ** token0Decimals;
             return FullMath.mulDiv(numerator1, numerator2, 1 << 192);
            }
```
