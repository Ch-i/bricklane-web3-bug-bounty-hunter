---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: No `address(0)` validation for `roleManager`
vuln_class: []
---

# No `address(0)` validation for `roleManager`

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

Across the protocol, several contracts set the role manager address in the `initialize ()` method. It is not validated if `roleManagerAddress` is `address(0)` or not. If `roleManager` is set as `address(0)`, it will be irreversible and a new contract will need to be created. 

Similarly, the method `setRoleManager()` needs to validate that the roleManagerAddress is not `address(0)`.

**Recommendation**: 

Add the validation for `initialize(...)` and `setRoleManager(...)` methods to check role manager is not set to address(0).
