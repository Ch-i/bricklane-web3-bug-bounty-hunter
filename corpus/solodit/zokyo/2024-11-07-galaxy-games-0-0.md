---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-11-07-galaxy-games-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-11-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md
tags:
- firm:zokyo
- report:2024-11-07-galaxy-games
title: Lack of a restriction on the recoverERC20() function in the pause status
vuln_class: []
---

# Lack of a restriction on the recoverERC20() function in the pause status

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-11-07-Galaxy Games.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md)_

---

**Severity** - Low

**Status** - Resolved

**Description**

Regarding the documentation, the recoverERC20() function is not supposed to be called while paused.
However, the function is missing a whenNotPaused modifier and it makes the function to be called in the pause status.

**Recommendation** 

Add a check to make sure that the return value is true and if not, revert the function.
