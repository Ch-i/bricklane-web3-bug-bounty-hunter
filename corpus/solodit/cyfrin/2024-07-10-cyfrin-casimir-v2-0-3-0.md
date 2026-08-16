---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Missing validations when initializing CasimirRegistry
vuln_class: []
---

# Missing validations when initializing CasimirRegistry

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** During Beacon Proxy deployment, CasimirRegistry can be deployed with 0 cluster size and 0 collateral.

**Recommended Mitigation:** Consider validating inputs for cluster size and collateral.

**Casimir:**
Mitigated in [37f3d34](https://github.com/casimirlabs/casimir-contracts/commit/37f3d34a9102478a85f6791774d86488bf5eb08e).

**Cyfrin:** Verified.
