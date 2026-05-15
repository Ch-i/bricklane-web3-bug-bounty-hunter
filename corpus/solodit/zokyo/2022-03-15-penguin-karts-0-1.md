---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-0-1
ingested_at: '2026-05-15T13:52:11Z'
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

StakingB_1.sol Line 614-615
First “updatePool” function executes “pool.lastRewardBlock = block.number;” and than
“pool.accTokenPerShare += (((block.number - pool.lastRewardBlock) * pool.rate...” where in
case of first operation “block.number” becomes equal to “pool.lastRewardBlock” their
sunstraction in next operation will always cause zero, that is the coefficient for the whole
equation. Pending rewards will never be increased.

**Recommendation**:

Place the first operation after the second.
