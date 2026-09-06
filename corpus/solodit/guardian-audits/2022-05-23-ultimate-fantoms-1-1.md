---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-1-1
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
title: UF-7 | Inaccurate Comments
vuln_class: []
---

# UF-7 | Inaccurate Comments

_Section severity (from Solodit section header): Low_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

On line 1712: `// random number between 0 to 4` is inaccurate as `_toEarn` takes on a random value of 0 or 1.
Additionally, on line 1672: `// 10%` is inaccurate as `_rndmAlloc` is calculated to be 15%.

**Recommendation**

Refactor comments to accurately reflect the code.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion.
