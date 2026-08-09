---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-1-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Unchecked return value
vuln_class: []
---

# Unchecked return value

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Low

**Status**:  Resolved

**Description**

In contract VariableBorrow.sol - return value of _updateInterest is not checked in almost all its occurrences.

**Recommendation**: 

Wrap the result of the call in a require statement or handle return according to the desired behavior for each particular case.
**Note #1**:   _updateInterest    no longer returns value
