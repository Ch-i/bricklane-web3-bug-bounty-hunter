---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Remove unnecessary imports and inheritance
vuln_class: []
---

# Remove unnecessary imports and inheritance

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Remove unnecessary imports and inheritance:
* `BurnStateManager` should only import and inherit from `Initializable`

**Remora:** Fixed in commit [8419903](https://github.com/remora-projects/remora-smart-contracts/commit/84199034d7255cfc90cd6eef502616a874f26908).

**Cyfrin:** Verified.

\clearpage
