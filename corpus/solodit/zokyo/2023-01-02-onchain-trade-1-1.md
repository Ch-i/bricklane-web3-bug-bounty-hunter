---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Unchecked possible zero address in VariableBorrow.sol
vuln_class: []
---

# Unchecked possible zero address in VariableBorrow.sol

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In contract VariableBorrow.sol, at lines 93 and 94 inside the constructor, the _swap and _oracle parameters can be zero and are not checked. 

**Recommendation**: 

Add a sanity check for the to address variable to not be zero and revert otherwise.
