---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-3-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: ReentrancyGuardUpgradeable is not used in CasimirFactory and CasimirRegistry
vuln_class: []
---

# ReentrancyGuardUpgradeable is not used in CasimirFactory and CasimirRegistry

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** CasimirRegistry and CasimirFactory inherit ReentrancyGuardUpgradeable but nonRentrant modifier is unused in bopth contracts.

**Recommended Mitigation:** Considering removing `ReentrancyGuardUpgradeable` inheritance in `CasimirRegistry` and `CasimirFactory`

**Casimir**
Fixed in [e403b8b](https://github.com/casimirlabs/casimir-contracts/commit/e403b8b86edbb96e02fd3f5e02e7f207890e1257)

**Cyfrin**
Verified.
