---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: No `amount(0)` validation for tokenAmount
vuln_class: []
---

# No `amount(0)` validation for tokenAmount

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract Pool.sol, the method `loop(...)` has a parameter `tokenAmount` which needs to be validated to be greater than 0.

**Recommendation**: 

Add the validation to check if `tokenAmount > 0` or not.
