---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: pausePlatform() have confusing naming
vuln_class: []
---

# pausePlatform() have confusing naming

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

contracts/MGD.sol#394, pausePlatform()
The function is named as a pausable function, though it works as a trigger function, because it
changes the state based on the previous value. Consider splitting it into 2 functions (pause()
and unpause()) or renaming e.g. triggerPause().

**Recommendation**:

Review the functionality, consider function renaming or split, correct the docstring for the
function. Also consider usage of the standard OpenZeppelin Pausable contract.
