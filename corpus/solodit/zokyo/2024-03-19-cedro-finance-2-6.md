---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: The unhandled returned value in `LiquidationManager`
vuln_class: []
---

# The unhandled returned value in `LiquidationManager`

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

The function `liquidate()` ignores the return value of `transferCeAmount` from `liquidate()` on line: 255. 

**Recommendation**: 

It is advised to add necessary require checks to validate and handle the returned value properly to avoid unintended issues.
