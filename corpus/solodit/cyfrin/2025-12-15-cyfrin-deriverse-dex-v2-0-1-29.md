---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-29
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing Trade Count Updates in `reversed_swap` Function for Buy Orders
vuln_class: []
---

# Missing Trade Count Updates in `reversed_swap` Function for Buy Orders

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `reversed_swap` function used for `buy` orders in `swap` operations fails to properly track and return `trade` counts, leading to incorrect trade statistics being written to the state. This inconsistency with `match_orders` causes buy order trades to be recorded as 0, resulting in inaccurate trading volume and trade count metrics.

In the `swap` flow, buy orders use `reversed_swap` while sell orders use `match_orders`.

```rust
    if buy {
        if price > px || engine.cross(price, OrderSide::Ask) {
            let total_fees;
            let remaining_sum;
            let input_sum = (data.amount as f64 / (1.0 + fee_rate)) as i64;

            (remaining_sum, traded_qty, total_fees) = engine.reversed_swap(price, input_sum)?;

```

There are 2 issues:

Issue 1: Missing `trades` Return Value

The `reversed_swap` function tracks trades internally but does not return this value:

```rust
            (remaining_sum, traded_qty, total_fees) = engine.reversed_swap(price, input_sum)?;
```

It returns `(remaining_sum, qty, total_fees)` but not `trades`, even though it maintains a trades variable internally.

Thus, the `trades` variable remains `0`, and this incorrect value is passed to `write_last_tokens`:

```rust
    if traded_qty > 0 && traded_sum > 0 {
        let candles = uninit_candles.init(&engine)?;
        engine.write_candles(candles, traded_qty, traded_sum)?;
        engine.write_last_tokens(traded_qty, traded_sum, trades, px)?;
    } else {
        bail!(DeriverseErrorKind::FailedToSwap {
            price,
            side: if buy { OrderSide::Ask } else { OrderSide::Bid }
        });
    }
```

Issue 2: Missing Trade Count Increment for AMM Trades
Unlike match_orders, reversed_swap does not increment `trades` after AMM transactions. In `match_orders`, every AMM trade increments the counter:

```rust
self.change_tokens(traded_qty, side)?;
self.change_mints(traded_mints, side)?;
self.log_amm(traded_qty, traded_mints, side);
self.set_px();
trades += 1;
```

However, in `reversed_swap`, AMM trades occur without incrementing `trades`:

```rust
self.change_tokens(traded_qty, side)?;
self.change_mints(traded_mints, side)?;
self.log_amm(traded_qty, traded_mints, side);
self.set_px();
total_fees = total_fees
    .checked_add((traded_mints as f64 * self.fee_rate) as i64)
    .ok_or(drv_err!(DeriverseErrorKind::ArithmeticOverflow))?;
break;
```

Similar omissions occur where AMM trades are executed without incrementing `trades`.



**Impact:**
- Incorrect trade statistics: Buy order trades are recorded as 0.
- Data inconsistency: Buy and sell orders are handled differently, causing asymmetric reporting.

**Recommended Mitigation:** Modify `reversed_swap` to return `trades` and increase `trades` after each AMM trade to be consistent with `match_orders`.

**Deriverse:** **Cyfrin:**
