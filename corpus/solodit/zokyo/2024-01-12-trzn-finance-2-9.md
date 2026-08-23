---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Unsafe Downcasting in `TokenStableV6_V2`
vuln_class: []
---

# Unsafe Downcasting in `TokenStableV6_V2`

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

There is unsafe downcasting on line: 483 and 492. 
```solidity
Line: 483             uint16 currentEpoch = uint16((block.number - epochStart) / epochTerm + 1);

Line: 492 	     return uint16((block.number - epochStart) / epochTerm + 1);
```
This can result in silent overflows or truncation of the number.

**Recommendation**: 

It is advised to use a safecast library such as that of Openzeppelin’s Safecast library.
