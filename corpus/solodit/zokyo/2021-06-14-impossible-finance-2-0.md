---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-impossible-finance-2-0
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
title: Explicitly mark visibility of state
vuln_class: []
---

# Explicitly mark visibility of state

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Impossible Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md)_

---

**Description**

StableXPair.sol The variables do not specify the visibility of the state. lines 34-42, 45, 46.

**Recommendation**:

Explicitly mark visibility of state.
