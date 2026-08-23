---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing ps check causes Dividend Loss
vuln_class: []
---

# Missing ps check causes Dividend Loss

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In the perp engine's fee distribution logic, both `match_ask_orders` and `match_bid_orders` functions allocate pool fees without checking if there is any liquidity provider in the spot pool. This causes a loss of dividends for DRVS token holders when there is no liquidity provider.

The code always allocates a portion of fees to `pool_fees` regardless of whether the `ps` is zero or not:

```rust
let delta = self.state.header.protocol_fees - prev_fees;
let pool_fees = ((1.0 - self.spot_pool_ratio) * delta as f64) as i64;
self.state.header.protocol_fees -= pool_fees;
self.state.header.pool_fees = self
    .state
    .header
    .pool_fees
    .checked_add(pool_fees)
    .ok_or(drv_err!(DeriverseErrorKind::ArithmeticOverflow))?;
```


**Impact:** When `ps == 0`, fees that should be 100% allocated to `protocol_fees` (for dividends) are incorrectly split, with `(1.0 - spot_pool_ratio) * delta` going to `pool_fees` instead.

DRVS token holders receive less in dividends than they should when there is no liquidity provider, as a portion of fees is incorrectly allocated to the pool.

**Recommended Mitigation:** Add a check for `ps == 0` before allocating pool fees in **both** `match_ask_orders()` and `match_bid_orders()` functions:

```rust
let delta = self.state.header.protocol_fees - prev_fees;
let pool_fees = if self.state.header.ps == 0 {
    0  // No pool allocation when there is no liquidity provider
} else {
    ((1.0 - self.spot_pool_ratio) * delta as f64) as i64
};
self.state.header.protocol_fees -= pool_fees;
self.state.header.pool_fees = self
    .state
    .header
    .pool_fees
    .checked_add(pool_fees)
    .ok_or(drv_err!(DeriverseErrorKind::ArithmeticOverflow))?;
```

This ensures that when there is no liquidity provider in the spot pool (`ps == 0`), all fees remain in `protocol_fees` and are properly distributed as dividends to DRVS token holders via the `dividends_allocation` function.

**Note**: This fix must be applied to **both** `match_ask_orders()` and `match_bid_orders()` functions, as they both contain the same buggy logic.

**Deriverse:** Fixed in commit [5dd59a](https://github.com/deriverse/protocol-v1/commit/5dd59a3c105207206c196c4abe06d53dc837426d).

**Cyfrin:** Verified.
