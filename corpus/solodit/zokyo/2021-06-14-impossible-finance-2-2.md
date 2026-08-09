---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-impossible-finance-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md
tags:
- firm:zokyo
- report:2021-06-14-impossible-finance
title: Extra variable
vuln_class: []
---

# Extra variable

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Impossible Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md)_

---

**Description**

StableXPair.sol line 177, 181. It is possible to optimize the code for lower gas consumption.
Immediately assign the blockTimestampLast value without using temporary variables.

**Recommendation**:
Set the blockTimestampLast value without using the blockTimestamp variable.
