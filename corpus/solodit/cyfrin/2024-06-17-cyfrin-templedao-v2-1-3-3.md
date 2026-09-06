---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: TempleGold incompatibility with some chains
vuln_class: []
---

# TempleGold incompatibility with some chains

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** Because of `PUSH0` not supported in 0.8.19 or lower versions of solidity compiler, TempleGold will be incompatible with chains like Linea where it only supports solidity compiler 0.8.19 or lower.

\clearpage
