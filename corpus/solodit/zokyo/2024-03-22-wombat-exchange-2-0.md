---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: Variable `lastSwapTimestamp` getting updated inside the loop
vuln_class: []
---

# Variable `lastSwapTimestamp` getting updated inside the loop

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract `VolatilePool.sol`, the method `_postSwapHook()`  has the following code:

```solidity
for (uint256 i; i < assetCount; ++i) {
           . . .
           marketPricesLast[asset] = marketPrice;
           lastSwapTimestamp = block.timestamp;
       }
```
Since `lastSwapTimestamp` needs to be updated once in the `_postSwapHook` method, there is no need to update it in the loop.

**Recommendation**: 

Update the variable `lastSwapTimestamp` outside the loop.
