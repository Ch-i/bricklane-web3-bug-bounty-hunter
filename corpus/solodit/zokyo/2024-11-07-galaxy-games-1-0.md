---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-11-07-galaxy-games-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-11-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md
tags:
- firm:zokyo
- report:2024-11-07-galaxy-games
title: Lack of return value check
vuln_class: []
---

# Lack of return value check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-11-07-Galaxy Games.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md)_

---

**Severity** - Informational

**Status** - Resolved

**Description**

The recoverERC20() function is missing a check for the return value of the token’s transfer.

**Recommendation** 

Add a check to make sure that the return value is true and if not, revert the function.
