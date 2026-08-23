---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-3
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
title: '`calculate_jump_price` returns a liquidity-over-asset ratio while three unit
  tests assert the inverse'
vuln_class: []
---

# `calculate_jump_price` returns a liquidity-over-asset ratio while three unit tests assert the inverse

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** `calculate_jump_price` computes a WAD-scaled liquidity-per-asset price:

```rust
price = normalized_liquidity_amount * 1e18 / normalized_asset_amount
```

The implementation is at `programs/bc-solana-jump-router-sc/src/utils/swap_utils.rs:26-59`. The swap logic compares this value directly against the backend-supplied `nbbo_price` when the standard operator path provides one.

Several unit tests in `#[cfg(test)]` still assert the inverse convention:

- `calculates_price_with_equal_decimals` passes `(asset=2_000_000, liquidity=1_000_000)` and expects `2e18`, but the liquidity-per-asset result is `0.5e18`.
- `supports_price_above_u64_max` passes `(asset=20, liquidity=1)` and expects `20e18`, but the liquidity-per-asset result is `0.05e18`.
- `supports_price_quotient_above_u128_max` comments that price scales with `asset_amount`, but the implemented formula divides by the normalized asset amount.

These tests are at `programs/bc-solana-jump-router-sc/src/utils/swap_utils.rs:91-129`.

**Impact:** Production code currently uses the liquidity-per-asset convention, but the tests document and assert the inverse for multiple cases. This creates maintenance risk: a future change could flip the production formula to satisfy the tests, or backend/event consumers could infer the wrong NBBO convention from the test suite.

**Recommended Mitigation:** Update the affected tests to assert the liquidity-per-asset formula, and add a short comment or function doc stating that `calculate_jump_price` returns WAD-scaled liquidity units per asset unit.

**Securitize:** Fixed in [8dd4999](https://github.com/securitize-io/bc-bd-router-sc/commit/8dd499989a96a23bdffe20ac9a5706a3abe70998).

**Cyfrin:** Verified.
