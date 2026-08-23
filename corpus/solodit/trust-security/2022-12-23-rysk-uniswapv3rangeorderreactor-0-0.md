---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-H-1 createUniswapRangeOrder() charges manager instead of pool
vuln_class: []
---

# TRST-H-1 createUniswapRangeOrder() charges manager instead of pool

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
**_createUniswapRangeOrder()** can be called either from manager flow, with **createUniswapRangeOrder()**, or pool-induced from **hedgeDelta()**. The issue is that the 
function assumes the sender is the parentLiquidityPool, for example:

```solidity
        if (inversed && balance < amountDesired) {
             // collat = 0
        uint256 transferAmount = amountDesired - balance;
         uint256 parentPoolBalance = 
             ILiquidityPool(parentLiquidityPool).getBalance(address(token0));
        if (parentPoolBalance < transferAmount) { revert 
            CustomErrors.WithdrawExceedsLiquidity(); 
        }
        SafeTransferLib.safeTransferFrom(address(token0), msg.sender, 
         address(this), transferAmount);
            } 
 ```
Balance check is done on pool, but money is transferred from sender. It will cause the order 
to use manager's funds. 

```solidity
    function createUniswapRangeOrder(
         RangeOrderParams calldata params,
             uint256 amountDesired
              ) external {
           require(!_inActivePosition(), "RangeOrder: active position");
         _onlyManager();
    bool inversed = collateralAsset == address(token0);
    _createUniswapRangeOrder(params, amountDesired, inversed);
    }
```
**Recommended Mitigation:**
Ensure safeTransfer from uses parentLiquidityPool as source.

**Team response:**
Fixed

**Mitigation Review:**
The transfers are now implemented in `_transferFromParentPool()` which ensures from is 
always parentLiquidityPool.
