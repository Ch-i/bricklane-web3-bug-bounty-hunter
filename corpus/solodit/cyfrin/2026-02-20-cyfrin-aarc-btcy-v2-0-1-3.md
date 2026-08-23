---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Batch processing can be DoS’d by cancellation/rescue of a single included request
  ID
vuln_class: []
---

# Batch processing can be DoS’d by cancellation/rescue of a single included request ID

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** The Hub’s batch processing functions (`IBTCYHub::processRedemptions` and `IBTCYHub::processSubscriptions`) iterate over arrays of request IDs and revert if any entry is invalid (e.g., the stored user is `address(0)`). Since requests can be removed via cancellation (and redemptions can also be removed via rescue), a request ID can become invalid after an operator has constructed a batch but before the batch transaction executes. Including that now-invalid ID causes the entire batch call to revert.

**Impact:** A single cancelled/rescued request can block processing of other valid requests included in the same batch, disrupting automated settlement pipelines and delaying unrelated subscriptions/redemptions until the batch is rebuilt and resubmitted.

**Recommended Mitigation:** Make batch processing tolerant to invalid/missing entries (skip + optionally emit an event), or provide single-item processing functions so operators can avoid batch-wide failure when individual requests are cancelled/rescued.

**Aarc Btcy:**
Fixed in [`ce0eb1e`](https://github.com/aarc-xyz/btcy-contracts-main/commit/ce0eb1eed40bd10b782dec85bcce2d4e206cded6)

**Cyfrin:** Verfied. Zero address entries now are skipped instead of reverting along with an event.
