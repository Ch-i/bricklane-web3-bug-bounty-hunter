---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-14
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Margin call detection functions ignore liquidation threshold
vuln_class: []
---

# Margin call detection functions ignore liquidation threshold

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `is_long_margin_call()` and `is_short_margin_call()` functions used to determine whether margin calls are active do not account for the `liquidation_threshold` parameter. This creates a discrepancy between when the system detects margin calls and when actual margin call occur.
```rust
pub fn is_long_margin_call(&self) -> bool {
    let root = self.long_px.get_root::<i128>();
    if root.is_null() {
        false
    } else {
        self.state.header.perp_underlying_px < (root.max_node().key() >> 64) as i64
    }
}

pub fn is_short_margin_call(&self) -> bool {
    let root = self.short_px.get_root::<i128>();
    if root.is_null() {
        false
    } else {
        self.state.header.perp_underlying_px > (root.min_node().key() >> 64) as i64
    }
}
```
Actual Liquidation Logic:
```rust
pub fn check_long_margin_call(&mut self) -> Result<i64, DeriverseError> {
    let mut trades = 0;
    // Applies liquidation threshold
    let margin_call_px = (self.state.header.perp_underlying_px as f64
        * (1.0 - self.state.header.liquidation_threshold)) as i64;

    loop {
        let root = self.long_px.get_root::<i128>();
        if root.is_null() || trades >= MAX_MARGIN_CALL_TRADES {
            break;
        }
        let node = root.max_node();
        let px = (node.key() >> 64) as i64;

        // Compares edge price to threshold-adjusted price
        if px > margin_call_px {
            // ... liquidation logic ...
        }
    }
    Ok(trades)
}
```
Same `liquidation_threshold` is applied during `check_short_margin_call` also.


Margin call remains false even when margin calls are occurring, which causes the following issues:
* The `perp_spot_price_for_withdrawal` freezing mechanism fails to activate when it should.
* In the perpetual withdrawal flow, `get_avail_funds` is called only with `margin_call` false.
* Rebalancing is invoked even during active margin-call conditions.

**Impact:** This allows users to withdraw more than they should during active margin calls, effectively bypassing the intended withdrawal restrictions.

**Recommended Mitigation:** Use the liquidation threshold into margin-call detection functions to ensure accurate margin-call detection and prevent incorrect withdrawal and rebalancing behavior.

**Deriverse:** Fixed in commit [4f7bc8](https://github.com/deriverse/protocol-v1/commit/4f7bc8ac68325aa93b339ff91c0ac794ea17ffd9).

**Cyfrin:** Verified.
