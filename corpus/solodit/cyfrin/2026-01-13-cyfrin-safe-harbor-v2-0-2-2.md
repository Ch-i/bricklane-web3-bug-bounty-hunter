---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Remove obsolete final `return` statement when already using named returns
vuln_class: []
---

# Remove obsolete final `return` statement when already using named returns

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** Remove obsolete final `return` statement when already using named returns:

* `AgreementFactory::create`

**SafeHarbor:**
Fixed in commit [220e5fb](https://github.com/PatrickAlphaC/safe-harbor/commit/220e5fb0af3f1750fd066a933f23f72124c37a6e).

**Cyfrin:** Verified.
