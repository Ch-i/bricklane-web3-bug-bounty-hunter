---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-1-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Incorrect value comparison for uint8 type in VariableBorrow.sol
vuln_class: []
---

# Incorrect value comparison for uint8 type in VariableBorrow.sol

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In contract VariableBorrow.sol, at line 521, 522 and 523 in function updateProtocolRevenue inside the require statements uint types are checked to be greater than or equal to 0, which is redundant as uint types can never be less than 0. The checks are meant to ensure that those values are in a certain range e.g [0, 100].

**Recommendation**: 

Remove the greater than or equal comparison and leave only the less than or equal to the range upper bound
