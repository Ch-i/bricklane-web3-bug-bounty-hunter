---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-28
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Redundant State Updates in `fill` Function Cause Issues
vuln_class: []
---

# Redundant State Updates in `fill` Function Cause Issues

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `fill` function contains **redundant state updates** to `last_asset_tokens` and `last_crncy_tokens` that are already properly handled by `write_last_tokens`. This redundancy causes data loss, incorrect accumulation, and state inconsistency when multiple orders are filled within the same slot.

- The Redundant Update
In the `fill` function, `last_asset_tokens` and `last_crncy_tokens` are redundantly updated:
```rust
self.state.header.last_asset_tokens = traded_qty;
self.state.header.last_crncy_tokens = traded_crncy;
```
After `match_orders` completes, `write_last_tokens` is already called with the accumulated values:

```rust
engine.write_last_tokens(traded_qty, traded_sum, trades, px)?;
```

The `write_last_tokens` function properly handles these state updates with:
- Slot boundary checking
- Accumulation logic when slots match
- Reset logic when slots differ

```rust
if self.state.header.slot == self.slot {
    self.state.header.last_crncy_tokens = self
        .state
        .header
        .last_crncy_tokens
        .checked_add(traded_crncy_tokens)
        .ok_or(drv_err!(DeriverseErrorKind::ArithmeticOverflow))?;
    self.state.header.last_asset_tokens = self
        .state
        .header
        .last_asset_tokens
        .checked_add(traded_asset_tokens)
        .ok_or(drv_err!(DeriverseErrorKind::ArithmeticOverflow))?;
} else {
    self.state.header.slot = self.slot;
    self.state.header.last_crncy_tokens = traded_crncy_tokens;
    self.state.header.last_asset_tokens = traded_asset_tokens;
}
```

Problems Caused by the Redundancy
- Data Loss in fill Loop: Within the `fill` function's loop, each iteration overwrites the previous values, only preserving the last order's values:
```
   while !order.is_null() && *remaining_qty > 0 {
       // ... process order ...
       self.state.header.last_asset_tokens = traded_qty;  // Overwrites previous value!
       self.state.header.last_crncy_tokens = traded_crncy; // Overwrites previous value!
   }
```
- Multiple fill Calls: The `match_orders` function can call `fill` multiple times, each overwriting the state with only partial data.

- Incorrect Accumulation: When `write_last_tokens` is subsequently called. If the slot matches, it adds the total accumulated values to the incorrectly set values from `fill`. This causes double counting or incorrect totals

Example: Before, the `last_asset_tokens = 200`, If `fill` sets `last_asset_tokens = 100` (last order only), then `write_last_tokens` adds the total `traded_qty = 500`, resulting in `600` instead of `200 + 500`.

**Impact:** Incorrect State: When `write_last_tokens` accumulates values, it adds to incorrectly set values, leading to wrong totals

**Recommended Mitigation:** Remove the redundant state updates from the `fill` function.

**Deriverse:** Fixed in commit [0be264f1](https://github.com/deriverse/protocol-v1/commit/0be264f1a0a727aa525ddab8d29c2a74c83294d7).

**Cyfrin:** Verified.
