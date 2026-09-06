---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-4-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Use `days` keyword for better readability
vuln_class: []
---

# Use `days` keyword for better readability

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** `TimeWeightedIncentiveLogic` currently declares the `MIN_INCREASE_DURATION` constant as `3 * 86400`. Instead, `3 days` should be used for better readability.

**Paladin:** Fixed by commit [`8eac91a`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/8eac91adcdc15f4f501c5f52724c2bbfe3f47e72).

**Cyfrin:** Verified. The `days` keyword is now used.

\clearpage
