---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-08-25-boba-network-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md
tags:
- firm:zokyo
- report:2022-08-25-boba-network
title: Variable declaration order in LzApp.
vuln_class: []
---

# Variable declaration order in LzApp.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-08-25-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md)_

---

**Description**

In contract LzApp.sol, at line 17 the variable failed Messages is declared after the internal function_NonblockingLzApp_init. Maintain a consistent order of variable and function declarations throughout the project.

**Recommendation**

Move the variable declaration to the top of the file, before any function declaration. Do this in all contract files.

**Re-audit comment**

Resolved
