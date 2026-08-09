---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-3-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: No method to unset a set router
vuln_class: []
---

# No method to unset a set router

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

In Contract Adapter.sol, the method `setRoute(...)` sets a route to be used but it can be unset in case the allowed route is compromised or not needed.

**Recommendation**: 

It is advised to add a method to unset a route if not needed
