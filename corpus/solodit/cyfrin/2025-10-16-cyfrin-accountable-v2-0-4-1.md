---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Consider consistently use `Ownable2Step`
vuln_class: []
---

# Consider consistently use `Ownable2Step`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** Currently some contracts use just Ownable, consider have all contracts use Ownable2Step to prevent accidental ownership loss.


**Accontable:**
Fixed in commit [`be75091`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/be7509165d468fd19bf48bab3fa87e565412a5b6)

**Cyfrin:** Verified.
