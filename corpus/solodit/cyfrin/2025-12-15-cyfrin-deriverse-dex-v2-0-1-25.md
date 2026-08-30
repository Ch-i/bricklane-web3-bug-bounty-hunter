---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-25
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: '`min_qty` Bypass via `IOC` limit order'
vuln_class: []
---

# `min_qty` Bypass via `IOC` limit order

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Spot orders compute the minimum order quantity `min_qty` from the user‐supplied limit price. An attacker can set an arbitrarily large limit price to drive `min_qty` down to a tiny value while the actual execution price is still clamped near the mark price. This bypasses the intended minimum order size enforcement for IOC orders.

`SpotParams::get_settings` enforces a ±12.5 % clamp on IOC prices via the `ipx` variable, but the minimum tokens are calculated from the original `px` argument (the user provided price) even when `IOC` mode is active:

```rust
        if ioc != 0 {
            if px < last_px - max_diff {
                ipx = last_px - max_diff;
            } else if px > last_px + max_diff {
                ipx = last_px + max_diff;
            } else {
                ipx = px;
            }
        } else if px < last_px - max_diff || px > last_px + max_diff {
            bail!(DeriverseErrorKind::InvalidPrice {
                price: px,
                min_price: last_px - max_diff,
                max_price: last_px + max_diff,
            });
        } else {
            ipx = px;
        }
...
        let min_tokens = min_qty(px, dc);
        // TODO remove
        if qty != 0 && qty.abs() < min_tokens {
            bail!(DeriverseErrorKind::InvalidQuantity {
                value: qty,
                min_value: min_tokens,
                max_value: SPOT_MAX_AMOUNT,
            });
        }
```

Because `min_qty` uses the unbounded px, **for bid orders**, an attacker can send `ioc != 0` with `LIMIT order` and choose an enormous `data.price`. `min_qty` then pulls a very small threshold from `PRICE_TOKENS`, allowing the attacker to submit dust-sized orders. The engine later clamps the executable price to within ±12.5 % of the mark, so the trade still goes through at the normal market price, but with an amount far below the intended minimum.

For example, the current price is `500_000_000`, the attacker/user can make `px=100_000_000_000_000` so that he can pay as little as `20_000`, making dust order.

**Impact:** Minimum order size limits for `IOC` orders can be bypassed. Attackers can generate large numbers of dust trades by supplying a large `data.price`.

**Recommended Mitigation:** Consider computing `min_qty` using the current market price.

**Deriverse:** Fixed in commit [134db8b](https://github.com/deriverse/protocol-v1/commit/134db8b1dac9e48641dac1a6b95bcf34637f695f).

**Cyfrin:** Verified.
