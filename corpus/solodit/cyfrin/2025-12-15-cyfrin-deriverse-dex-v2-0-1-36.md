---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-36
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Insurance fund decrease when `margin_call_penalty_rate` is less than `rebates_rate`
vuln_class: []
---

# Insurance fund decrease when `margin_call_penalty_rate` is less than `rebates_rate`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** When `margin_call_penalty_rate` is less than `rebates_rate`(`fee_rate * REBATES_RATIO`), the insurance fund decreases instead of increasing during margin calls.

During a margin call, the insurance fund is updated as: `perp_insurance_fund += (new_fees - rebates)`, where:
- `new_fees = traded_crncy * margin_call_penalty_rate`
- `rebates = traded_crncy * fee_rate * REBATES_RATIO`

If `margin_call_penalty_rate < fee_rate * REBATES_RATIO`, then `(new_fees - rebates)` becomes negative, causing the insurance fund to decrease when it should increase.

**Impact:** The insurance fund can be drained during margin calls instead of being replenished.

**Recommended Mitigation:** Ensure that `margin_call_penalty_rate >= fee_rate * REBATES_RATIO` to guarantee that margin call penalties always contribute positively to the insurance fund.

**Deriverse:** Fixed in commit [1ef948](https://github.com/deriverse/protocol-v1/commit/1ef948af18b47f3e502d0054d760212d4b6263f1).

**Cyfrin:** Verified.



\clearpage
