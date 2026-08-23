---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing Validation for `order_type` in NewSpotOrderData
vuln_class: []
---

# Missing Validation for `order_type` in NewSpotOrderData

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `NewSpotOrderData::new` validation function does not verify that `order_type` is a valid value for spot orders. While spot orders should only accept `Limit (0)` and `Market (1)`, the validation allows `MarginCall (2)` and `ForcedClose (3)` to pass through. These invalid values are then incorrectly processed as Market orders, leading to data inconsistency in logs and potential confusion.

In `src/program/instruction_data.rs`, the `NewSpotOrderData::new` function validates:
- `instr_id range
- price validity (only when `order_type == 0`)
- `amount` range
However, it does not validate that `order_type` is within the allowed range for spot orders (0 or 1).

```rust
    fn new(instruction_data: &[u8], instr_count: u32) -> Result<&Self, DeriverseError> {
        let data = bytemuck::try_from_bytes::<Self>(instruction_data)
            .map_err(|_| drv_err!(InvalidClientDataFormat))?;

        if data.instr_id >= instr_count {
            bail!(InvalidInstrId { id: *data.instr_id })
        }
        if data.order_type == 0 && !(MIN_PRICE..=MAX_PRICE).contains(&data.price) {
            bail!(InvalidPrice {
                price: data.price,
                min_price: MIN_PRICE,
                max_price: MAX_PRICE,
            })
        }
        if !(1..=SPOT_MAX_AMOUNT).contains(&data.amount) {
            bail!(InvalidQuantity {
                value: data.amount,
                min_value: 1,
                max_value: SPOT_MAX_AMOUNT,
            })
        }

        return Ok(data);
    }
```

The `OrderType` enum defines:
```rust
pub enum OrderType {
    Limit = 0,
    Market = 1,
    MarginCall = 2,    // Only for perp orders
    ForcedClose = 3,   // Not used in codebase
}
```

In `src/program/processor/new_spot_order.rs`, the code only explicitly handles Limit:
```rust
if data.order_type == OrderType::Limit as u8 {
    data.price
} else if buy {
    mark_px + (mark_px >> 3)  // All other values treated as Market
} else {
    mark_px - (mark_px >> 3)
}
```

Then the `type` is being emitted in logs:

```rust
    solana_program::log::sol_log_data(&[bytemuck::bytes_of::<SpotPlaceOrderReport>(
        &SpotPlaceOrderReport {
            tag: log_type::SPOT_PLACE_ORDER,
            order_type: data.order_type,
            side: if buy { 0 } else { 1 },
            ioc: data.ioc,
            client_id: client_state.id,
            order_id: engine.state.header.counter,
            instr_id: data.instr_id,
            qty: data.amount,
            price,
            time: ctx.time,
        },
    )]);
```

**Impact:**
- Data Inconsistency: Logs will contain incorrect order_type values that don't match the actual order behavior
- Input Validation Gap: Missing validation allows invalid enum values to be accepted

**Recommended Mitigation:** Add validation in `NewSpotOrderData::new` to ensure `order_type` is only 0 (Limit) or 1 (Market) for spot orders:

Example:
```rust
        // Add this validation
        if data.order_type > OrderType::Market as u8 {
            bail!(InvalidOrderType {
                order_type: data.order_type,
                allowed_types: vec![OrderType::Limit as u8, OrderType::Market as u8],
            })
        }
```

**Deriverse:** Fixed in commit [53000a3](https://github.com/deriverse/protocol-v1/commit/53000a32c4f9af1629b8a9f7d9b6b696a6084189).

**Cyfrin:** Verified.
