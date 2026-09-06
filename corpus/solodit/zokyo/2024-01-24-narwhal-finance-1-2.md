---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Pairs `feeIndex` and `groupIndex` can not be updated 0
vuln_class: []
---

# Pairs `feeIndex` and `groupIndex` can not be updated 0

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

In Contract PairInfos.sol, the method updatePair(...) has the following check:


```solidity
       if (_pair.feeIndex > 0) {
           p.feeIndex = _pair.feeIndex;
       }


       if (_pair.groupIndex > 0) {
           p.groupIndex = _pair.groupIndex;
       }

```

Here if owner wants to set feeIndex and/or groupIndex to 0, it will not be set without reverting leading to owner believing values are set properly.

**Recommendation**: 

Remove the check if feeIndex > 0 and/or groupIndex > 0.
