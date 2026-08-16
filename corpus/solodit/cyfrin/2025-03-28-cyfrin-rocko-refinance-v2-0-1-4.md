---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-1-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Insufficient data length validation in `onMorphoFlashLoan`
vuln_class: []
---

# Insufficient data length validation in `onMorphoFlashLoan`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** `RockoFlashRefinance::onMorphoFlashLoan` performs a basic check on the length of the `data` parameter, requiring it to be at least 20 bytes. However, this check is insufficient as the actual data being sent is much larger, containing multiple addresses, strings, and an Id parameter. The minimum expected data length should be at least 256 bytes plus additional bytes for dynamic string data.

**Recommended Mitigation:**
```diff
-        require(data.length >= 20, "Invalid data");
+        require(data.length >= 256, "Invalid data");
```

**Rocko:** Fixed in commit [1da67d7](https://github.com/getrocko/onchain/commit/1da67d7f3ae8076a6cc135ef9a6e5595ad6e29a2).

**Cyfrin:** Verified.
