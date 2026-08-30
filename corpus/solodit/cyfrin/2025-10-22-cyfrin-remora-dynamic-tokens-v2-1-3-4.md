---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: In `FiveFiftyRule` add check that `equity != 0` in functions `createEntity`
  and `setCatalyst`
vuln_class: []
---

# In `FiveFiftyRule` add check that `equity != 0` in functions `createEntity` and `setCatalyst`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** If `equity` is ever set to zero then `_checkEntityAllowance` will revert on division by zero which will prevent all transfers that pass through the code paths involving `_checkEntityAllowance`.

This will occur any time a transfer involves a transfer to a `to` address which is
- part of a group with an individual that is a catalyst
- is an individual that is a catalyst

**Impact:** Minimal. Reverts will happen until an admin calls `setCatalyst` to update the `equity` to a non-zero value.

**Remora:** Fixed at commit [511e7da](https://github.com/remora-projects/remora-dynamic-tokens/commit/511e7da2038e669f628c8232fd8f37c1e6798fab).

**Cyfrin:** Verified.

\clearpage
