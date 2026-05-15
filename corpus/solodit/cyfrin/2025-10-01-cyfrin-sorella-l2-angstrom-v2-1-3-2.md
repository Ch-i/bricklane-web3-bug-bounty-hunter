---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Unused custom error should removed if not required
vuln_class: []
---

# Unused custom error should removed if not required

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `AngstromL2` defines the `NegationOverflow()` custom error; however, it is not currently used and so should be removed unless actually required.

**Sorella Labs:** Fixed in commit [4702d84](https://github.com/SorellaLabs/l2-angstrom/commit/4702d84d6ea9c6346467be261cedfca02f1e0d36).

**Cyfrin:** Verified.
