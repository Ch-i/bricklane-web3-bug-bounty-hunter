---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-11-15-milestonebased-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-11-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-11-15-milestoneBased.md
tags:
- firm:zokyo
- report:2021-11-15-milestonebased
title: Event Withdrawn from Roadmap contract should index the recipient address too,
  to be able to filter based on it.
vuln_class: []
---

# Event Withdrawn from Roadmap contract should index the recipient address too, to be able to filter based on it.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-11-15-milestoneBased.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-11-15-milestoneBased.md)_

---

**Recommendation**:
Make the recipient parameter indexed in the Withdrawn event.
