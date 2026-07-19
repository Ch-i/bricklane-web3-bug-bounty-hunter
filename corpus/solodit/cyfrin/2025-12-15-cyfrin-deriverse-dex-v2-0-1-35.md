---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-35
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
title: Margin call uses stale edge price
vuln_class: []
---

# Margin call uses stale edge price

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `check_long_margin_call` and `check_short_margin_call` functions determine whether positions should be liquidated based on edge prices retrieved from the price trees before applying funding rate updates and rebalancing. This causes positions to be liquidated using stale edge prices that don't reflect the current state after funding rate changes, leading to unfair liquidations.

`check_funding_rate` and `check_soc_loss` are called after the liquidation decision is made, but these functions can modify the user’s funds, which directly affects whether liquidation should occur.

```rust
pub fn check_long_margin_call(&mut self) -> Result<i64, DeriverseError> {
    let mut trades = 0;
    let margin_call_px = (self.state.header.perp_underlying_px as f64
        * (1.0 - self.state.header.liquidation_threshold)) as i64;

    loop {
        let root = self.long_px.get_root::<i128>();
        if root.is_null() || trades >= MAX_MARGIN_CALL_TRADES {
            break;
        }
        let node = root.max_node();
        let px = (node.key() >> 64) as i64;  // Gets stale edge price

        if px > margin_call_px {  // Decision made with stale price
            let temp_client_id = ClientId(node.link());

            // Funding rate checked AFTER liquidation decision
            self.check_funding_rate(temp_client_id)?;
            self.check_soc_loss(temp_client_id)?;

            // ... liquidation logic ...

            // Edge price updated AFTER liquidation
            self.change_edge_px(temp_client_id);
        }
    }
}
```


**Impact:** Users may be liquidated when they should not be, resulting in unnecessary loss of funds.

**Recommended Mitigation:** Consider using the updated edge price, after applying the `check_funding_rate` and `check_soc_loss` to determine whether the position should be liquidated.

**Deriverse:** Fixed in commit [1efef6](https://github.com/deriverse/protocol-v1/commit/1efef63dfea11c8e031d1fe1fb0b48875a856153).

**Cyfrin:** Verified.
