---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: Over-complicated design of delegation
vuln_class: []
---

# Over-complicated design of delegation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** In staking contract, the logic around delegation is over-complicated, where it has concepts of `delegation`, `self-delegation`, and `delegation to self`, of these logic mixed, which could be simplified.
