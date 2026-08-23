---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Unconstrained for-loop
vuln_class: []
---

# Unconstrained for-loop

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In TradingStorage.sol - Method unregisterPendingMarketOrder() starts with a for loop that iterates for a number of times depending on the length of orderIds. The length of the array can go indefinitely since there is no size constraint is applied in method storePendingMarketOrder() which could check first the size of the array so that it does not pass a certain limit.

**Recommendation** 

-EnumerableSet can be used to replace uint[] as the type of orderIds. This helps to get the index i which has the value of _id in O(1) so that the for-loop is not needed in this case.
Another solution is to set a limit on the array contained in the mapping pendingOrderIds[trader] so that the for-loop does not grow indefinitely.
**Fix**: Dev team utilized EnumerableSet to avoid the unconstrained for-loop.
