---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Use named returns where this eliminates a local variable and especially for
  `memory` returns
vuln_class: []
---

# Use named returns where this eliminates a local variable and especially for `memory` returns

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Use named returns where this eliminates a local variable and especially for `memory` returns:
* `TokenBank::viewAllFees`

**Remora:** Fixed in commit [6602423](https://github.com/remora-projects/remora-smart-contracts/commit/66024232cfea24b69bd055086f8088d40f3d1d4a).

**Cyfrin:** Verified.
