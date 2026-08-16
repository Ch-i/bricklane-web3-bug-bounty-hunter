---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-11-07-galaxy-games-1-3
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
title: Unnecessary use of nonReentrant modifier
vuln_class: []
---

# Unnecessary use of nonReentrant modifier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-11-07-Galaxy Games.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-07-Galaxy%20Games.md)_

---

**Severity** - Informational

**Status** - Resolved

**Description**

The burn() and recoverERC20() functions have the nonReentrant modifiers but the functions could not have reentrancy attacks because the functions can only be called by the owner and _burn() function doesn’t have an implementation to cause the reetrancy.
Unnecessary use of modifiers will result in unnecessary gas consumption.

**Recommendation** 

Remove the nonReentrant modifier in the functions and delete the ReentrancyGuard import in the contract.
