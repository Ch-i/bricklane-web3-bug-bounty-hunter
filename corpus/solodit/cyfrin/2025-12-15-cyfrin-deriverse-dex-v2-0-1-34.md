---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-34
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing Update of `perp_spot_price_for_withdrowal` in `perp_withdraw` Function
vuln_class: []
---

# Missing Update of `perp_spot_price_for_withdrowal` in `perp_withdraw` Function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `perp_withdraw` function fails to update the `perp_spot_price_for_withdrowal` field(including `perp_long_spot_price_for_withdrowal` and `perp_short_spot_price_for_withdrowal` in later commits) when there is no margin call, while other similar functions (`new_perp_order` and `perp_quotes_replace`) properly update this field. This inconsistency can lead to stale price data being used in subsequent margin call scenarios, potentially affecting withdrawal calculations.

The `perp_spot_price_for_withdrowal` field is used by the `get_avail_funds` function when calculating available funds during margin call situations. The field should be updated to the current `perp_underlying_px` when there is no margin call to ensure accurate calculations in future operations.

We can see that in `new_perp_order` and `perp_quotes_replace`:

```rust
    if !long_margin_call {
        engine.state.perp_long_spot_price_for_withdrowal = engine.state.perp_underlying_px;
    }
    if !short_margin_call {
        engine.state.perp_short_spot_price_for_withdrowal = engine.state.perp_underlying_px;
    }
```

Now, in `perp_withdraw`, we are having:

```rust
let margin_call = engine.is_long_margin_call() || engine.is_long_margin_call();
if !margin_call {
    engine.check_rebalancing()?;
}
```

**Impact:** The `perp_spot_price_for_withdrowal` field(including `perp_long_spot_price_for_withdrowal` and `perp_short_spot_price_for_withdrowal` in later commits) may retain stale values if `perp_withdraw` is called without a margin call, while other functions update it. If a margin call occurs after a `perp_withdraw` operation (in the same transaction or subsequent transactions), the `get_avail_funds` function may use an outdated price when `margin_call=true`, leading to incorrect available funds calculations.

**Recommended Mitigation:** Add the missing update to maintain consistency and price up-to-date.

**Deriverse:** Fixed in commit [66c878](https://github.com/deriverse/protocol-v1/commit/66c878370dc8041d6544b8fdee636102ce00fe8c).

**Cyfrin:** Verified.
