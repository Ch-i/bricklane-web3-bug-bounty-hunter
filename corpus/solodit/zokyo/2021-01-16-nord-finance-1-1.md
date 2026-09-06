---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-01-16-nord-finance-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-01-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md
tags:
- firm:zokyo
- report:2021-01-16-nord-finance
title: package.json, development dependency added to dependencies.
vuln_class: []
---

# package.json, development dependency added to dependencies.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-01-16-Nord Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md)_

---

**Recommendation**:

It is expected that development dependencies should be located in devDependency.
