---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: Zero addresses not checked in contracts constructors
vuln_class: []
---

# Zero addresses not checked in contracts constructors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** In constructors of `DaiGoldAuction`, `TempleGold`, and `TempleGoldStaking` contracts, zero addresses are not validated.
