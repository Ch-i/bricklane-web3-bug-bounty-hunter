---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-0-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: Rounding bias in `calculate_jump_price()` skews `max_positive_slippage_mbps`
  enforcement across swap directions
vuln_class: []
---

# Rounding bias in `calculate_jump_price()` skews `max_positive_slippage_mbps` enforcement across swap directions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The `max_positive_slippage_mbps` protection relies on `calculate_jump_price()`, which always rounds the computed price down via integer division. Because the protection compares `jump_price` against `nbbo_price` in opposite directions for the two swap flows, using the same rounding direction in both cases introduces inconsistent enforcement across swap directions.

`calculate_jump_price()` derives a WAD-scaled price by dividing two normalized integers:

```rust
// Calculate price with WAD scale
let price = U256::from(normalized_liquidity_amount)
    .checked_mul(U256::from(10u128.pow(WAD_SCALE as u32)))
    .ok_or_else(|| error!(JumpRouterError::MathOverflow))?
    .checked_div(U256::from(normalized_asset_amount))
    .ok_or_else(|| error!(JumpRouterError::MathOverflow))?;
```

This uses integer division and therefore always floors the result.

The floored `jump_price` is then used for `max_positive_slippage_mbps` enforcement in both swap directions:

```rust
if let Some(nbbo_price) = nbbo_price_opt {
    if jump_price < *nbbo_price {
        let price_improvement_mbps =
            utils::swap_utils::calculate_price_improvement_mbps(&jump_price, nbbo_price)?;
        require!(
            price_improvement_mbps <= jump_router_state.max_positive_slippage_mbps,
            JumpRouterError::MaxPositiveSlippageExceeded
        );
    }
}
```

```rust
if let Some(nbbo_price) = nbbo_price_opt {
    if jump_price > *nbbo_price {
        let price_improvement_mbps =
            utils::swap_utils::calculate_price_improvement_mbps(nbbo_price, &jump_price)?;
        require!(
            price_improvement_mbps <= jump_router_state.max_positive_slippage_mbps,
            JumpRouterError::MaxPositiveSlippageExceeded
        );
    }
}
```

This creates inconsistent behavior across swap directions:

- In the `LiquidityForAsset` path, the guard evaluates positive slippage when `jump_price < nbbo_price`, so flooring affects the comparison in one direction.
- In the `AssetForLiquidity` path, the guard evaluates positive slippage when `jump_price > nbbo_price`, so the same flooring affects the comparison in the opposite direction.

The issue does not affect the direct `min_amount_out_net` user slippage check, but it does undermine the correctness of the separate positive-slippage guard.

**Impact:** The configured `max_positive_slippage_mbps` limit is not enforced consistently across swap directions. This weakens the reliability of the control and can produce behavior that diverges from operator expectations and off-chain risk assumptions.

**Recommended Mitigation:** If keeping the current scalar-price approach, use direction-specific conservative rounding for the enforcement path.

**Securitize:** Fixed in [27e9c64](https://github.com/securitize-io/bc-bd-router-sc/commit/27e9c640d43e1ae81963605d7d6343bdd72d08fc) and [7757b81](https://github.com/securitize-io/bc-bd-router-sc/commit/7757b81d8f4e4eb31aa883eec5663214f05ccafe).

**Cyfrin:** Verified.
