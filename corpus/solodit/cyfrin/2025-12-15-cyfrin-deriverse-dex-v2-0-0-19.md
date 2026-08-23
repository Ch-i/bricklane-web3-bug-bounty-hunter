---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-19
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
title: Spot price manipulation can lead to unfair liquidations
vuln_class: []
---

# Spot price manipulation can lead to unfair liquidations

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** When perpetual instruments are configured without an oracle feed, the system uses the spot market's `last_px` as the `perp_underlying_px` for liquidation calculations. The spot price (`last_px`) can be manipulated through order book orders or AMM trades, allowing attackers to trigger unfair liquidations of healthy perpetual positions. This vulnerability enables malicious actors to force liquidations at manipulated prices, causing significant financial losses to users.

When no oracle is configured, the spot price directly becomes the perpetual underlying price:

Liquidations are triggered based on the manipulated `perp_underlying_px`:

```rust
pub fn check_long_margin_call(&mut self) -> Result<i64, DeriverseError> {
    let margin_call_px = (self.state.header.perp_underlying_px as f64
        * (1.0 - self.state.header.liquidation_threshold)) as i64;

    // If edge_px > margin_call_px, position gets liquidated
    // ...
}

pub fn check_short_margin_call(&mut self) -> Result<i64, DeriverseError> {
    let margin_call_px = (self.state.header.perp_underlying_px as f64
        * (1.0 + self.state.header.liquidation_threshold)) as i64;

    // If edge_px < margin_call_px, position gets liquidated
    // ...
}
```

**Impact:** The impact is high, as healthy positions may be liquidated unfairly. Additionally, an attacker may be able to exploit this behavior for profit.

**Recommended Mitigation:** Consider using an external oracle or TWAP.

**Deriverse:** Fixed in commit [fc0013](https://github.com/deriverse/protocol-v1/commit/fc0013bc5add2c0ad0eac3f31bfc37f32c87c07c).

**Cyfrin:** Verified.



\clearpage
