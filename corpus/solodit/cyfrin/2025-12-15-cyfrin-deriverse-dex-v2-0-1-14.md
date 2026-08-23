---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-14
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
title: Referral discount is not applied when `fees_prepayment` is zero in `PerpEngine::fill`
vuln_class: []
---

# Referral discount is not applied when `fees_prepayment` is zero in `PerpEngine::fill`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In `PerpEngine::fill`, when `fees_prepayment` is zero we do not apply the referral discount even though we still send `ref_payment` to `ref_address`.

```rust
                if *fees_prepayment == 0 {
                    let fee = (traded_crncy as f64 * self.fee_rate) as i64;
                    taker_info.sub_funds(fee).map_err(|err| drv_err!(err))?;
                    fee
                } else {
```

`self.fee_rate` is equal to `perp_fee_rate`.

**Impact:** The user is required to pay additional funds due to the referral discount not being applied, causing a loss to the user.


**Recommended Mitigation:** Instead of charging `self.fee_rate`, we should charge the fee rate after applying the referral discount, `(1.0 - args.ref_discount) * self.fee_rate`.



**Deriverse:** Fixed in commit [91bffc](https://github.com/deriverse/protocol-v1/commit/91bffc86cf2e6e441ca8a526d68808dbc19a122a).

**Cyfrin:** Verified.
