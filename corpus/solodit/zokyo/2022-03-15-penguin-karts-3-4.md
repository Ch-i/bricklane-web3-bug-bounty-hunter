---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-03-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md
tags:
- firm:zokyo
- report:2022-03-15-penguin-karts
title: Code could be simplified.
vuln_class: []
---

# Code could be simplified.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

StakingB_1.sol Line 609
“pool.lastRewardBlock = block.number” can be executed before condition so this operation
shouldn’t be repeated twice in the code.

**Recommendation**:

Use just one realisation of “pool.lastRewardBlock = block.number” before condition.
