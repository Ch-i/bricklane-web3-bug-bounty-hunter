---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Missing bracket in docs
vuln_class: []
---

# Missing bracket in docs

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Description:** [The document](https://goldilocks-1.gitbook.io/goldidocs/locks/the-price-function) is missing a bracket.
```diff
- Market price = Floor Price + ((PSL/Supply)*(FSL+PSL/FSL)^6)
+ Market price = Floor Price + (PSL/Supply)*((FSL+PSL)/FSL)^6
```

**Client:** Acknowledged, this has been corrected.

**Cyfrin:** Acknowledged.
