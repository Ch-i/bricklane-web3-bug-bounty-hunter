---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-L-2 Insufficient dust checks
vuln_class: []
---

# TRST-L-2 Insufficient dust checks

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
In `hedgeDelta()`, there is a dust check in the case of sell wETH order:
```solidity
        // sell wETH
             uint256 wethBalance = inversed ? amount1Current : amount0Current;
        if (wethBalance < minAmount) return 0;
```
However, the actual used amount is _delta

```solidity
             uint256 deltaToUse = _delta > int256(wethBalance) ? wethBalance : 
           uint256(_delta);
        _createUniswapRangeOrder(rangeOrder, deltaToUse, inversed);
```
The check should be applied on deltaToUse rather than wethBalance because it will be the 
minimum of wethBalance and _delta.
Additionally, there is no corresponding check for minting with collateral in case **_delta** is 
negative.

**Recommended Mitigation:**
Correct current dust checks and add them also in the if clause.

**Team Response:**
This feature is more useful on ethereum mainnet than L2 will consider if it makes sense to 
implement dust check on collateral size as well

**Mitigation review:**
The dust check is now applied on **deltaToUse**. It is up to the project if they wish to perform a 
dust check when **_delta** is negative.
