---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Use unchained initializers instead
vuln_class: []
---

# Use unchained initializers instead

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** The direct use of initializer functions rather than their unchained equivalents should be avoided to prevent [potential duplicate initialization](https://docs.openzeppelin.com/contracts/5.x/upgradeable#multiple-inheritance).

**Strate:**
Fixed in commit [def7d36](https://github.com/Strata-Money/contracts/commit/def7d360225f49662c73bf968d63d935c82d9d0e).

**Cyfrin:** Verified.
