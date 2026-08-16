---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: Method `toLogScale` should be internal
vuln_class: []
---

# Method `toLogScale` should be internal

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

In Library DynamicFeeHelper, the method `toLogScale(...)` has the following logic:
```solidity
// bound the result
       if (result > type(int32).max) {
           return type(int32).max;
       } else if (result < type(int32).min) {
           return type(int32).min;
       } else {
           return int32(result);
       }
```
Here the result is greater than `type(int32).max`, then returned value is `type(int32).max` which incorrect if `toLofScale()` method is used directly. Any external contract relying on this value can consider the upper and lower bounds as the correct result and process accordingly which will lead to wrong calculations.

**Recommendation**: 

Update to make this method internal and to be used only through `safetoLogScale()` method.
