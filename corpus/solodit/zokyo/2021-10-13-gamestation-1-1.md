---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-10-13-gamestation-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2021-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-10-13-Gamestation.md
tags:
- firm:zokyo
- report:2021-10-13-gamestation
title: There is the possibility to use modifier whenNotPaused from the Pausable contract
  in the contract GameStationToken function _beforeTokenTransafer instead of required
  in line 42.
vuln_class: []
---

# There is the possibility to use modifier whenNotPaused from the Pausable contract in the contract GameStationToken function _beforeTokenTransafer instead of required in line 42.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-10-13-Gamestation.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-10-13-Gamestation.md)_

---

**Recommendation**:

Add modifier whenNotPaused to the _ beforeTokenTransafer function.
