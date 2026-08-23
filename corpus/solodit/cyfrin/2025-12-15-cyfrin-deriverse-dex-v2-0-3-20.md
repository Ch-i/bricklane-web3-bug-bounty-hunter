---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-20
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Incorrect Boundary Condition in `check_pool_fees` Function Excludes Valid Minimum
  Token Transactions
vuln_class: []
---

# Incorrect Boundary Condition in `check_pool_fees` Function Excludes Valid Minimum Token Transactions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `check_pool_fees` function uses a strict greater-than (`>`) comparison when checking if `tokens_qty` meets the `min_tokens` requirement. This incorrectly excludes the valid boundary case where `tokens_qty` equals `min_tokens`, preventing legitimate pool fee conversions when the calculated quantity exactly matches the minimum allowed value.

In `src/program/spot/engine.rs`, the `check_pool_fees` function contains the following condition:

```rust
pub fn check_pool_fees(
    &mut self,
    client_state: &mut ClientPrimaryState,
    rest_of_order: &mut i64,
    traded_sum: &mut i64,
    price: i64,
    min_tokens: i64,
) -> DeriverseResult {
    let mints_qty = self.state.header.pool_fees >> 1;
    let tokens_qty = (self.state.header.asset_tokens as f64 * mints_qty as f64
        / self.state.header.crncy_tokens as f64) as i64;
    if tokens_qty > min_tokens && *rest_of_order > min_tokens + tokens_qty {
        // ... execute pool fee conversion logic
    }
    Ok(())
}
```

This violates with other parts of the code, like:

```rust
    if !(data.order_type == OrderType::Market as u8 || data.ioc != 0) && data.amount < min_tokens {
        bail!(InvalidQuantity {
            value: data.amount,
            min_value: min_tokens,
            max_value: SPOT_MAX_AMOUNT
        })
    }
```

**Impact:** Valid pool fee conversions are incorrectly rejected when the calculated tokens_qty exactly equals min_tokens, reducing the efficiency of pool fee utilization

**Recommended Mitigation:** Change the comparison operator from `>` to `>=` to include the valid boundary case.

**Deriverse:** Fixed in commit [3a24de8](https://github.com/deriverse/protocol-v1/commit/3a24de8933a2f1f9b039224d89857f857c2fdfc6).

**Cyfrin:** Verified.
