---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-12
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: Combined internal and external fees are not capped
vuln_class: []
---

# Combined internal and external fees are not capped

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The program validates each fee manager independently, but it does not enforce a maximum total fee across both the internal router fee and the optional external fee. Each `FeeManager` is individually validated against `MAX_FEE_NUMERATOR`, which currently allows up to 50% per fee manager. This means a swap can apply two individually valid fee managers whose combined fee exceeds the intended maximum fee limit.

**Impact:** The effective fee charged to users can be higher than the protocol’s intended maximum. In the worst case, most or all of the fee-denominated liquidity amount may be consumed by fees. Although `min_amount_out` can protect users when configured correctly, the protocol itself does not enforce the combined-fee invariant.

**Recommended Mitigation:** Validate the combined internal and external fee rate before executing the swap.
For example, expose the fee numerator from each FeeManager, or add a method to validate combined fee managers:
```rust
require!(
    internal_fee_numerator + external_fee_numerator <= MbpsFeeManager::MAX_FEE_NUMERATOR,
    JumpRouterError::MaxFeeExceeded
);
```

**Securitize:** Acknowledged.

\clearpage
