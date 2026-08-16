---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-1-2
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
title: Unnecessary event emission when configuration values do not change
vuln_class: []
---

# Unnecessary event emission when configuration values do not change

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** `RockoFlashRefinance::updateFee` updates the `ROCKO_FEE_BP` variable and emits a `FeeUpdated` event regardless of whether the new fee value is different from the current one. This leads to unnecessary event emissions when the owner calls the function with the same fee value that is already set.
The function `pauseContract` can be improved similarly too.

**Rocko:** Fixed in commit [99a73dc](https://github.com/getrocko/onchain/commit/99a73dc20fce34811c224fdd46b7e173748bfeb8).

**Cyfrin:** Verified.
