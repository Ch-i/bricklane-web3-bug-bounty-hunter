---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-06-08-yield-farming-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-06-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md
tags:
- firm:zokyo
- report:2022-06-08-yield-farming
title: In contract UnifarmNFTManagerUpgradeable, function stakeOnUnifarm, variable
  farmToken it’s an user input that represents an address that it is not sanitized
  before, this lead to re- entracy attacks and unpredictable behaviours.
vuln_class: []
---

# In contract UnifarmNFTManagerUpgradeable, function stakeOnUnifarm, variable farmToken it’s an user input that represents an address that it is not sanitized before, this lead to re- entracy attacks and unpredictable behaviours.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-06-08-Yield Farming.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md)_

---

**Recommendation**:

Whitelist the farmToken address or ad re-entracy attacks to the stake and burn function and
the other functions that modified the same state data that the stake function does. (Done)
