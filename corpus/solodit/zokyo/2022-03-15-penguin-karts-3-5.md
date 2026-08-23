---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-3-5
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
title: Use constants.
vuln_class: []
---

# Use constants.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

StakingB.sol Lines 17, 18, 19
StakingB_1.sol Lines 518
If the value of the storage variable can’t be changed it can be set as constant in order to save
gas.

**Recommendation**:

Set offered storage as constant
