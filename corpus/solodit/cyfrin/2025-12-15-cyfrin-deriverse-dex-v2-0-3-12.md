---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-12
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Rounding Error Accumulation in Partial Order Fills Leads to Unfair Cost Distribution
vuln_class: []
---

# Rounding Error Accumulation in Partial Order Fills Leads to Unfair Cost Distribution

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Note:**
This finding was submitted after careful consideration. The impact is negligible in practice, as it only manifests when an order is partially filled multiple times, causing tiny rounding errors to accumulate. However, it is still worth documenting, as it represents a systematic bias that could potentially be addressed in documentation or future improvements.

**Description:** When an order is partially filled multiple times, rounding errors from the `trade_sum` function accumulate in the order's remaining `sum` field. The final fill receives the accumulated rounding errors, causing the last trader to pay more than they should based on the actual traded quantity.

The vulnerability exists in the `fill` function of the spot trading engine. When an order is created, the total currency value is calculated using `trade_sum(price, qty)` and stored in `order.sum`:

```rust
// Line 643: Order creation
let order_sum = self.trade_sum(price, qty)?;
// ...
sum: order_sum,  // Stored in order
```


The `trade_sum` function performs floating-point multiplication with `rdf` (rounding division factor) and truncates to `i64`:

```rust
// Lines 157-158: rdf calculation
let df = state.header.dec_factor as f64;
let rdf = 1f64 / df;  // rdf is typically a decimal (e.g., 0.1, 0.01, 0.001)

// Lines 277-284: trade_sum function
fn trade_sum(&self, a: i64, b: i64) -> Result<i64, DeriverseError> {
    let sum = (a as f64 * b as f64) * self.rdf;  // Floating-point multiplication with rdf
    // ...
    Ok(sum as i64)  // Truncation from f64 to i64 causes rounding errors
}
```


**Root Cause of Rounding Errors:**
The rounding errors occur because:
1. `rdf = 1.0 / dec_factor`, where `dec_factor = 10^n` (a power of 10 based on token decimal differences)
2. `rdf` could be a decimal fraction (e.g., 0.1, 0.01, 0.001), requiring floating-point arithmetic
3. The multiplication `(a * b) * rdf` in floating-point can produce results that are not exactly representable as integers
4. The conversion from `f64` to `i64` truncates the fractional part, causing precision loss
5. Without `rdf` (i.e., if `rdf = 1.0`), the calculation would be exact integer arithmetic with no rounding errors


When an order is partially filled (line 1187), the code recalculates the currency value using `trade_sum`:

```rust
// Lines 1178-1188
let (traded_qty, traded_crncy, last) = if order_qty <= *remaining_qty {
    (order_qty, order.sum(), false)  // Full fill uses stored sum
} else {
    (*remaining_qty, self.trade_sum(*remaining_qty, px)?, true)  // Partial fill recalculates
};
```


Then, when `last = true` (partial fill), the code decrements the order's sum:

```rust
// Lines 1265-1267
if last {
    order.decr_qty(traded_qty).map_err(|err| drv_err!(err))?;
    order.decr_sum(traded_crncy).map_err(|err| drv_err!(err))?;  // Subtracts recalculated value
    // ...
}
```


**The Problem:**
1. The presence of `rdf` (a decimal fraction) in `trade_sum` causes floating-point precision issues when converting to `i64`.
2. Each partial fill recalculates `trade_sum(remaining_qty, px)`, which introduces rounding errors due to `f64→i64` truncation in the presence of `rdf`.
3. The recalculated value is subtracted from `order.sum`, causing rounding errors to accumulate in the remaining `sum`.
4. When the order is fully filled, the remaining `order.sum` may not equal `trade_sum(remaining_qty, px)` but instead contains all accumulated rounding errors from previous partial fills.


**Example Scenario:**
Assume `rdf = 0.1` (i.e., `dec_factor = 10`) and price = 99:
- Order: qty=100, price=99, rdf=0.1
- Original sum: `trade_sum(100, 99) = (100 * 99) * 0.1 = 990.0` → `990` (exact)
- First partial fill (33 qty): `traded_crncy = trade_sum(33, 99) = (33 * 99) * 0.1 = 326.7` → `326` (truncated, loses 0.7)
- Remaining sum: `990 - 326 = 664` (should be 663.3, but stored as integer)
- Second partial fill (33 qty): `traded_crncy = trade_sum(33, 99) = 326.7` → `326` (truncated, loses 0.7)
- Remaining sum: `664 - 326 = 338` (should be 337.3, but stored as integer)
- Final fill (34 qty):
  - Expected: `trade_sum(34, 99) = (34 * 99) * 0.1 = 336.6` → `336`
  - Actual received: `order.sum = 338` (contains accumulated rounding errors: 0.7 + 0.7 = 1.4)
  - The final trader receives `338` instead of `336`, paying `2` more than they should

**Impact:** **Unfair Cost Distribution**: The last trader to fill a partially-filled order bears the cost of all accumulated rounding errors from previous partial fills.

**Recommended Mitigation:** This may be a design choice, and leaving it as-is is acceptable. However, it should be clearly documented that rounding errors are unavoidable when using floating-point arithmetic with `rdf`, and the current implementation accumulates these errors to the final partial fill,
Given the negligible impact and the fact that rounding errors are unavoidable (the question is only who bears them), **the current design choice is acceptable as long as it is properly documented.**

**Deriverse:** Fixed in commit [058c856](https://github.com/deriverse/protocol-v1/commit/058c8565a6394ac0ce0cba8841c523db51d5f8a5).

**Cyfrin:** Verified. Added documents.
