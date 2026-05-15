---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-30
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing `change_funding_rate` Call After Price Update in `perp_mass_cancel`
  and `perp_order_cancel`
vuln_class: []
---

# Missing `change_funding_rate` Call After Price Update in `perp_mass_cancel` and `perp_order_cancel`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In `perp_order_cancel` and `perp_mass_cancel functions`, the code updates the underlying price (`perp_underlying_px`) via `set_underlying_px` but fails to call `change_funding_rate` before invoking `check_rebalancing`(and potentially `mass_cancel`), which internally calls `check_funding_rate`. This results in funding rate calculations being performed with stale global funding rate values that haven't been updated to reflect the new underlying price(even though the price is correctly updated), potentially leading to incorrect funding fee calculations for users.

The funding rate mechanism works as follows:
- `change_funding_rate` updates the global funding rate state
```rust
    pub fn change_funding_rate(&mut self) {
        let time_delta = self.time - self.state.header.perp_funding_rate_time;
        if time_delta > 0 && self.state.header.perp_price_delta != 0.0 {
            self.state.header.perp_funding_rate +=
                ((time_delta as f64) / DAY as f64) * self.state.header.perp_price_delta;
        }
        self.state.header.perp_price_delta =
            (self.market_px() - self.state.header.perp_underlying_px) as f64 * self.rdf;
        self.state.header.perp_funding_rate_time = self.time;
    }
    /*
```
- `check_funding_rate` applies the global funding rate to individual clients:
```rust
    pub fn check_funding_rate(&mut self, temp_client_id: ClientId) -> Result<bool, DeriverseError> {
        let info = unsafe { &mut *(self.client_infos.offset(*temp_client_id as isize)) };
        let info5 = unsafe { &mut *(self.client_infos5.offset(*temp_client_id as isize)) };
        let perps = info.total_perps();
        let mut change = false;
        if perps != 0 {
            if self.state.header.perp_funding_rate != info5.last_funding_rate {
                let funding_funds = -(perps as f64
                    * (self.state.header.perp_funding_rate - info5.last_funding_rate))
                    .round() as i64;
```

Thus the `perp_funding_rate` should be refreshed each time before `check_funding_rate` is called.

The issue is that in the `perp_order_cancel` and `perp_mass_cancel`:

```rust
// perp_order_cancel
engine.state.set_underlying_px(accounts_iter)?;
// ... order cancellation logic ...
engine.check_rebalancing()?;  // Calls check_funding_rate() internally

// perp_mass_cancel
engine.state.set_underlying_px(accounts_iter)?;
engine.mass_cancel(client_state.temp_client_id)?;  // Calls check_funding_rate() at line 1888
// ... margin call checks ...
engine.check_rebalancing()?;  // Also calls check_funding_rate() at line 2363
```

When `perp_underlying_px` is updated but `change_funding_rate` is not called, the global `perp_funding_rate` may not reflect the latest price changes.

**Impact:** Users may be charged incorrect funding fees when canceling orders, as the funding rate calculations use stale global funding rate values that don't reflect the updated underlying price since the `change_funding_rate` is not called.

**Recommended Mitigation:** Add `change_funding_rate` calls immediately after `set_underlying_px` in both vulnerable functions.

**Deriverse:** Fixed in commit [74f9650](https://github.com/deriverse/protocol-v1/commit/74f9650ef966b422d95a384bb1e39f4f7bd9cf22).

**Cyfrin:** Verified.
