---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Index returned overwrites an existing element
vuln_class: []
---

# Index returned overwrites an existing element

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In TradingStorage.sol - Methods: firstEmptyTradeIndex, firstEmptyOpenLimitIndex() returns index = 0 if all the array slots are occupied. This in turn overrides the first element (i.e. 0).

**Recommendation** 

Revert if all occupied (i.e. 3 by default) open limit slots are full.

**Fix** -   As of  commit a72e06b ,  A variable allOccupied is added in order to revert if all slots are full. Therefore issue is resolved.
