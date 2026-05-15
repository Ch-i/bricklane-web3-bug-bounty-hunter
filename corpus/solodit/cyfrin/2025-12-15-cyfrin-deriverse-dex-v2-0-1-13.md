---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-13
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
title: Slippage Guard Could be Too Loose For Leveraged Perp Markets
vuln_class: []
---

# Slippage Guard Could be Too Loose For Leveraged Perp Markets

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Perpetual “market” orders fall back to the same hard-coded `±12.5 %` price cap that is used for spot orders. While that cap is arguably acceptable for spot, it is dangerously loose for leveraged perp trading: a user can be filled up to 12.5 % away from the reference price in one shot, magnifying losses by the user’s leverage factor. There is no ability to tighten this slippage or enforce a stricter cap when leverage is high.

In `new_perp_order.rs`, non-limit buys default to `px + (px >> 3)` and sells to `px - (px >> 3)`, i.e. ±12.5 % of the current underlying price.

```rust
    let (price, min_tokens) = PerpParams::get_settings(
        if data.order_type == OrderType::Limit as u8 {
            data.price
        } else if buy {
            px + (px >> 3)
        } else {
            px - (px >> 3)
        },
        data.amount,
        if buy { OrderSide::Bid } else { OrderSide::Ask },
        px,
        data.ioc,
        engine.dc,
    )?;
```

Spot orders reuse the same ±12.5 % window, which is acceptable because spot positions are unleveraged.

Perp orders, however, can be levered up to the protocol maximum (`MAX_PERP_LEVERAGE`). Filling a leveraged market order at `−12.5 % (or +12.5 %)` immediately consumes a large portion of the user’s margin and can nearly trigger unintended liquidation during extreme market conditions, even when the user was intended to trade near the mark price.

Also, users have no way to configure a tighter cap unless they avoid market orders altogether (use `limit+IOC`), which is unrealistic—many traders still expect market orders to have reasonable slippage protection.

**Impact:** Under volatile or thin-liquidity conditions, leveraged traders who rely on market orders can be executed at very unfavorable prices (up to `12.5 %` away), leading to outsized losses or incoming instant liquidations.

**Recommended Mitigation:** Ultimately the team should decide how strict to be, but the current 12.5 % blanket cap is out of line with leveraged-market risk management and should be tightened.

If possible, implement leverage-aware slippage caps (e.g., shrink tolerance as leverage increases) or allow users to specify a custom slippage limit, with a protocol-defined maximum.

Another recommendation is to benchmark major CEX/DEX perp products to choose a safer default.

**Deriverse:** Fixed in commit [b2ff47aa](https://github.com/deriverse/protocol-v1/commit/b2ff47aa00fc88daec2eb15339751e27fb23a723).

**Cyfrin:** Verified.
