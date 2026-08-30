---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`AllowList::hasTradeRestriction` mutability should be set to `view`'
vuln_class: []
---

# `AllowList::hasTradeRestriction` mutability should be set to `view`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `AllowList::hasTradeRestriction` does not make any changes to storage, it simply reads some variables and makes some checks, but the function's mutability is not marked as view.

**Recommended Mitigation:** Change mutability to view.

**Remora:** Fixed in commit [81faadb](https://github.com/remora-projects/remora-smart-contracts/commit/81faadbd3baa1deec950db08abf635c5a277a7c5).

**Cyfrin:** Verified.
