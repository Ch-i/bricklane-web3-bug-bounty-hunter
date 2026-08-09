---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-12
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Referral Incentives Disabled for All Legitimate Users During Any Liquidation
vuln_class: []
---

# Referral Incentives Disabled for All Legitimate Users During Any Liquidation

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Once the engine detects any instrument that requires liquidation (`is_long_margin_call` or `is_short_margin_call`), the `margin_call` flag is set to true for every subsequent `new_perp_order`. This flag is passed unchanged into `match_{ask,bid}_orders`, which disables referral payouts while it is `true`. As a result, all users— even those submitting normal orders unrelated to the liquidation — stop receiving/producing referral rewards for as long as any liquidation candidate remains. This global switch was likely intended only for actual liquidation trades.

In `new_perp_order.rs` the code sets `margin_call = engine.is_long_margin_call() || engine.is_short_margin_call();`

```rust
    let margin_call = engine.is_long_margin_call() || engine.is_short_margin_call();
    if !margin_call {
        engine.state.header.perp_spot_price_for_withdrowal = engine.state.header.perp_underlying_px;
    }
```

That boolean is forwarded to `PerpEngine::match_{ask,bid}_orders` via `MatchOrdersStaticArgs`

```rust
        if engine.cross(price, OrderSide::Ask) {
            (remaining_qty, _, ref_payment) = engine.match_ask_orders(
                Some(&mut client_community_state),
                &MatchOrdersStaticArgs {
                    price,
                    qty: data.amount,
                    ref_discount,
                    ref_ratio: header.ref_program_ratio,
                    ref_expiration: header.ref_program_expiration,
                    ref_client_id: header.ref_client_id,
                    trades_limit: 0,
                    margin_call,
                    client_id: client_state.temp_client_id,
                },
            )?;
        }
```

Referral rebates are conditioned on `!args.margin_call in perp_engine.rs`: when `margin_call` is `true`, ref_payment is forced to zero.
```rust
        let ref_payment = if self.time < args.ref_expiration && !args.margin_call {
            ((fees - rebates) as f64 * args.ref_ratio) as i64
        } else {
            0
        };
```

Liquidation routines (`check_long_margin_call, check_short_margin_call`) also pass `margin_call: true` explicitly, but there is no distinction between liquidation-triggered fills and ordinary orders.
```rust
    if buy {
        if engine.check_short_margin_call()? < MAX_MARGIN_CALL_TRADES {
            engine.check_long_margin_call()?;
        }
    } else if engine.check_long_margin_call()? < MAX_MARGIN_CALL_TRADES {
        engine.check_short_margin_call()?;
    }
```

Therefore, the presence of any liquidation candidate globally blocks referral rewards for all traders, regardless of who is being liquidated.


**Impact:** Legitimate users lose their expected referral incentives whenever any other account is under liquidation. Although not an immediate loss of funds, it represents a systemic incentive failure affecting all participants during stressed periods.

**Recommended Mitigation:** Restrict the `margin_call` flag to trades that are actually part of liquidation flows.

**Deriverse:** Fixed in commit [bc9bd6](https://github.com/deriverse/protocol-v1/commit/bc9bd6ab49dd15dcf2c3d83559fa4ad0bd6777d9).

**Cyfrin:** Verified.
