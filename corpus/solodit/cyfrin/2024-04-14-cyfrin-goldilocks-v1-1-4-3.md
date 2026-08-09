---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-4-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Augmented assignment operator costs more gas than normal addition for state
  variables.
vuln_class: []
---

# Augmented assignment operator costs more gas than normal addition for state variables.

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

Normal addition operation (`x=x+y`) costs less gas than augmented assignment operator (`x+=y`) for state variables (113 gas). (34 instances)
