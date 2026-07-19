---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-paid-ignition-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md
tags:
- firm:zokyo
- report:2021-06-14-paid-ignition
title: Undocumented “magic” number
vuln_class: []
---

# Undocumented “magic” number

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Paid Ignition.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md)_

---

**Description**

IgnitionCore.sol, 37.
Variable status_boolean is initialized just once during the construction and is not changed
anywhere. Consider declaring it as a constant in order to save gas. Also, the variable has
“magic value” - undicumented hardcoded number. Consider adding the comment or
documentation to the constant.

**Recommendation**:

Declare the variable as constant and add documentation.
