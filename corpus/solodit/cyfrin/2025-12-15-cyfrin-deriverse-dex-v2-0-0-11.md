---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-11
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Makers' rebates are not paid in case of swap
vuln_class: []
---

# Makers' rebates are not paid in case of swap

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** When orders are matched, we choose between AMM and orderbook based on which offers better prices. In case of `swap` when orderbook doesnt exist, we trade with only AMM, when it exists we choose better of both.. we create a temporary client's primary account.. while looking for available orders we pass `client-community` as [`none`](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/processor/swap.rs#L180)
```rust
//inside swap.rs
    if buy {
        if price > px || engine.cross(price, OrderSide::Ask) {
            (q, traded_sum, trades, _) =
                engine.match_orders(price, qty, &mut client_state, None, OrderSide::Ask)?;
        }
```
inside `engine.rs`'s `match_orders()` function, `fee-rate & ref-discounts` are [zero](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/spot/engine.rs#L1370) because `client-community` was `None`
```rust
        let fill_static_args = FillStaticArgs {
            fee_rate,
            ref_discount,
            taker_client_id: client.id,
            side,
        };
```
Incase when orderbook offered better prices, we go through that route.. inside `match_orders()`; [here](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/spot/engine.rs#L1463)
```rust
                   if remaining_qty > 0 {
                        self.fill(
                            &mut line,
                            &mut remaining_qty,
                            &mut sum,
                            &mut trades,
                            &mut total_fees,
                            &mut total_rebates,
                            &mut fees_prepayment,    // 0
                            &fill_static_args, // contains fee rate as 0
                            //ref_discount,
                            //client.id,
                            //fee_rate,
                            //side,
                        )?;
                    }
                }
```
Inside `fill()`, since we had [`fill_static_args.fee_rate == 0.0`](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/spot/engine.rs#L1218) we dont charge/deduct fee and dont give rebates to makers because both(fee rate and rebates) came out to be [zero](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/spot/engine.rs#L1219) in this case.... Makers's orders are filled without receiving rebate and user traded without paying protocol fee.
```rust
            let (fees, rebates) = if fill_static_args.fee_rate == 0.0 {
                (0, 0)
            } else {
                (
                    self.get_fees(
                        fees_prepayment,
                        traded_crncy,
                        fill_static_args.fee_rate,
                        fill_static_args.ref_discount,
                    )?,
                    ((traded_crncy as i128 * self.rebates_rate) >> DEC_PRECISION) as i64,
                )
            };
```

**Impact:** Protocol loses intended fees from swaps & makers dont receive rebates.

**Recommended Mitigation:** Change the current condition to this:
```rust
let (fees, rebates) = if self.fee_rate == 0.0 {
    (0, 0)
} else {
    (
        self.get_fees(
            fees_prepayment,
            traded_crncy,
            fill_static_args.fee_rate,
            fill_static_args.ref_discount,
        )?,
        ((traded_crncy as i128 * self.rebates_rate) >> DEC_PRECISION) as i64,
    )
};
```
**Deriverse**
Fixed in commit: [b368de](https://github.com/deriverse/protocol-v1/commit/b368de93d68a635ddca7355ad9f81a69102f66d9)

**Cyfrin:** Verified.
