---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Remove obsolete check in `updateFee`
vuln_class: []
---

# Remove obsolete check in `updateFee`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Remove obsolete check in `updateFee`:
```diff
-        require(newFee >= 0, "Fee must not be negative");
```

This check is obsolete since `newFee` is declared as `uint256` therefore cannot be negative.

**Rocko:** Fixed in commit [2c50838](https://github.com/getrocko/onchain/commit/2c50838a5cc5e498a14874a5d3348da20087e6bc).

**Cyfrin:** Verified.
