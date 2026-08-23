---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-03-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md
tags:
- firm:zokyo
- report:2022-03-15-penguin-karts
title: Code structure is messed up.
vuln_class: []
---

# Code structure is messed up.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

StakingB_1.sol Line 524
Storage and events must be separated in order to make code structure more readable.

**Recommendation**:

Move the “amountOfUser” variable to the other variables.
