---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Cache storage slots to prevent identical storage reads
vuln_class: []
---

# Cache storage slots to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** Cache storage slots to prevent identical storage reads if the values don't change during execution.

For example, `Bet::accept,cancel,resolve` should cache `_aavePool` if it is likely to be non-zero since this saves 1 storage read in `accept` and 2 storage reads in `resolve,cancel`.

**WannaBet:** Fixed in commit [b8b4863](https://github.com/gskril/wannabet-v2/commit/b8b4863960cc3eeee3ccf017e4ac3d26f65959fe).

**Cyfrin:** Verified.
