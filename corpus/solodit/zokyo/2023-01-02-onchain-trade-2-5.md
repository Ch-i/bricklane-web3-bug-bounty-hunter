---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-2-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Prefixed variable name
vuln_class: []
---

# Prefixed variable name

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In contract Swap.sol, at line 102 the variable of type IBorrowForSwap is prefixed with the “$” sign. This is not considered naming best practice in Solidity and is not ideal for readability.

**Recommendation**: 

Remove the “$” prefix
