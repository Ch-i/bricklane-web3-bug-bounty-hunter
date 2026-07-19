---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-03-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md
tags:
- firm:zokyo
- report:2022-03-15-penguin-karts
title: Logic issue.
vuln_class: []
---

# Logic issue.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

StakingB_1.sol Line 512
“lastRewardBlock” must be initialized when the pool is set. In other case first reward will be
counted as a reward in range [0; last block number] that is a numerous amount.

**Recommendation**:

Initialize lastRewardBlock in pool setting.
