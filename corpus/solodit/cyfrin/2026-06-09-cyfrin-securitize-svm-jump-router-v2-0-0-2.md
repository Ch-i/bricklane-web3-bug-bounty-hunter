---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-0-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: Protocol fee is charged on the gross amount instead of the post-external-fee
  remainder
vuln_class: []
---

# Protocol fee is charged on the gross amount instead of the post-external-fee remainder

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** FR-2 specifies that when both the stored Securitize fee and an optional external fee apply to a swap, the external fee is deducted first and the Securitize fee is then applied only to the remaining amount. The current implementation deducts both fees, but computes each one from the same gross input rather than charging the Securitize fee on the post-external-fee remainder.

This finding's primary proof is the buy path, where both fees are calculated from `amount_in`:

```rust
let liquidity_fee_amount = jump_router_state.fee_manager.calculate_fee(amount_in)?;
let liquidity_external_fee_amount = match external_fee_manager {
    Some(manager) => manager.calculate_fee(amount_in)?,
    None => 0,
};
let liquidity_swap_amount = amount_in
    .checked_sub(liquidity_fee_amount)
    .and_then(|x| x.checked_sub(liquidity_external_fee_amount))
    .ok_or(JumpRouterError::MathOverflow)?;
```

The same gross-before-external ordering also appears in the current sell implementation, where both fees are computed from the full `quoted_liquidity_amount`:

```rust
let liquidity_fee_amount = jump_router_state
    .fee_manager
    .calculate_fee(quoted_liquidity_amount)?;

let liquidity_external_fee_amount = match external_fee_manager {
    Some(manager) => manager.calculate_fee(quoted_liquidity_amount)?,
    None => 0,
};
```

The spec-conformant sequence is:

1. `external_fee_amount = external_rate * gross`
2. `securitize_fee_amount = securitize_rate * (gross - external_fee_amount)`
3. `jump_input = gross - external_fee_amount - securitize_fee_amount`

The implemented sequence computes the Securitize fee on `gross` rather than on `gross - external_fee_amount`, so the Securitize fee is slightly larger than FR-2 intends whenever an external fee is present.

**Impact:** The effect is a deterministic overcollection of the Securitize fee on external-fee swaps, equal to `securitize_rate * external_fee_amount`. At realistic fee rates this is a small, second-order amount — for example, a 1% Securitize fee and a 1% external fee on a gross of 1,000,000 overcharges by roughly 100 units (`0.01 * 10,000`), i.e. about 0.01% of notional. The magnitude only becomes material if both fee rates are configured near the 50% per-fee cap, since each manager is validated independently against that cap.

**Recommendation:**

Apply FR-2 literally on both swap paths: compute the external fee first, subtract it, then compute the stored Securitize fee on the remainder.

**Securitize:** Acknowledged; This is a doc bug.
