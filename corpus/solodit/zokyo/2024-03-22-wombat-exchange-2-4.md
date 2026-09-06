---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: Unnecessary cast
vuln_class: []
---

# Unnecessary cast

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract VolatilePool.sol, the method `_postSwapHook()` has the following logic:

```solidity
           int256 value = DynamicFeeHelper.safeToLogScale((marketPrice * 1e18) / priceLast, dt);


           DynamicFeeHelper.write(dynamicFeeData[asset], uint40(block.timestamp), int32(value));
```
Here, the value returned is of type int32 but unnecessarily cast to int256 and again cast to int32 on the next line.

**Recommendation**: 

Remove the unnecessary cast and get the return value as int32.
