---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-1-11
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: RS-3 | Repetitive Function Calls
vuln_class: []
---

# RS-3 | Repetitive Function Calls

_Section severity (from Solodit section header): Low_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

In the `receive` and `fallback` functions the `random` function is called several times, even though the random value is constant during each tx.

**Recommendation**

Compute the random value once.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion.
