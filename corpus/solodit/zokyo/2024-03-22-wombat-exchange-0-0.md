---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: The latest `Value` is not saved in the `Write()` method
vuln_class: []
---

# The latest `Value` is not saved in the `Write()` method

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In Library DynamicFeeHelper, the method `write(...)` is called to write data after each swap.
Since the timepoint for a block can be written only once, this method has the following condition for early return:
```solidity
PointHistory memory lastPoint = pointHistories[lastIndex];
       if (lastPoint.pointTimestamp == blockTimestamp) {
           // Early return if we've already written a timepoint this block
           lastPoint.value = value; 
           return lastIndex;
       }
```
Here, `lastPoint.value` is being updated but `lastPoint` is of type `memory` so the value will not be persisted in the storage. Hence latest value will not be saved.

Since this `value` is the first step of the data flow and the swap method can be called multiple times in a block, this not being persistent can lead to unexpected results in further calculation. 

**Recommendation**: 

Update the `value` for `lastIndex` properly so it is persistent.
