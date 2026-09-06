---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-12
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Misleading revert message
vuln_class: []
---

# Misleading revert message

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In PairsStorage.sol - Modifier feedOk() contains a misleading revert message in
```solidity
require(_feed.feedCalculation != FeedCalculation.COMBINE, "FEED_2_MISSING");
```
**Recommendation** 

Change the error message returned to describe what actually went on in this faulty transaction.

**Fix** -  As of  commit a72e06b ,  Issue is resolved by changing the revert message to be a better match for the context.
