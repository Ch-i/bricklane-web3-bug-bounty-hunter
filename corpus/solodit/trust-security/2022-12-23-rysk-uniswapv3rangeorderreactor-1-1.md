---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-M-2  Hedging won't work if token1.decimals() < token0.decimals()
vuln_class: []
---

# TRST-M-2  Hedging won't work if token1.decimals() < token0.decimals()

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
`tickToToken0PriceInverted()` performs some arithmetic calculations. It's called by 
`_getTicksAndMeanPriceFromWei()`, which is called by `hedgeDelta()`. This line can overflow:

```solidity
    uint256 intermediate = inWei.div(10**(token1.decimals() -
         token0.decimals()));
```
Also, this line would revert even if the above calculation was done correctly:

```solidity
    meanPrice = OptionsCompute.convertFromDecimals(meanPrice, 
         token0.decimals(), token1.decimals());
```

```solidity
    function convertFromDecimals(uint256 value, uint8 decimalsA, uint8 decimalsB) internal pure
        returns (uint256) {
    if (decimalsA > decimalsB) {
          revert();
        }
        …
```
The impact is that when `token1.decimals()` < `token0.decimals()`, the contract's main function 
is unusable.

**Recommended Mitigation:**
Refactor the calculation to support different decimals combinations. Additionally, add more 
comprehensive tests to detect similar issues in the future.

**Team Response:**
Fixed

**Mitigation Review**
The code has been refactored, there is no longer risk of overflow.
