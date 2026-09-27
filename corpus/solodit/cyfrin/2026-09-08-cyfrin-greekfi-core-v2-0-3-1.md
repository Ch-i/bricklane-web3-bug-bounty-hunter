---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-3-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`Factory::createOptions, createOptions2` copy read-only batch inputs into
  memory'
vuln_class: []
---

# `Factory::createOptions, createOptions2` copy read-only batch inputs into memory

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Factory::createOptions, createOptions2` are external entry points whose dynamic array parameters are read-only, but the arrays are declared as `memory`. The ABI decoder therefore copies the complete arrays from calldata before the loops use them. The cost grows with every batched market and salt.

**Recommended Mitigation:** Declare the external batch parameters as `calldata` and refactor the shared creation logic so each entry can be consumed without copying the entire arrays into memory. Ensure the internal helper boundary also accepts calldata-compatible input; otherwise the copy is merely moved into each loop iteration.

**GreekFi:** Fixed in [PR33](https://github.com/greekfi/contracts/pull/33)

**Cyfrin:** Verified. Factory now keeps read-only creation parameters and batch arrays in calldata through the shared creation path.
