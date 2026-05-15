---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-01-26-graviton-zero-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-01-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-01-26-Graviton%20Zero.md
tags:
- firm:zokyo
- report:2022-01-26-graviton-zero
title: Code structure is messed up.
vuln_class: []
---

# Code structure is messed up.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-01-26-Graviton Zero.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-01-26-Graviton%20Zero.md)_

---

**Description**


StakingB_1.sol Line 524
Storage and events must be separated in order to make code structure more readable.

**Recommendation**:

Move the “amountOfUser” variable to the other variables.
