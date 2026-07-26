---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing Slippage Protection in Market Seat Buy/Sell Operations
vuln_class: []
---

# Missing Slippage Protection in Market Seat Buy/Sell Operations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `buy_market_seat()` and `sell_market_seat()` functions calculate seat prices dynamically based on the current `perp_clients_count` at execution time, but provide no slippage protection. Users cannot specify maximum/minimum acceptable prices, exposing them to unexpected price changes.

In `buy_market_seat()`, the seat price is calculated as:

```rust
let seat_price = PerpEngine::get_place_buy_price(
    instrument.perp_clients_count,
    instrument.crncy_token_decs_count,
)?;

instrument.seats_reserve += seat_price;
let price = data.amount + seat_price;
// ... price is deducted without validation
client_state.sub_crncy_tokens(price)?;
```

Similarly, in `sell_market_seat()`, the sell price is calculated:

```rust
let seat_price = PerpEngine::get_place_sell_price(
    instrument.perp_clients_count,
    instrument.crncy_token_decs_count,
)?;

client_state.add_crncy_tokens(seat_price)?;
```

The price calculation functions (`get_place_buy_price()` and `get_place_sell_price()`) use a bonding curve model where the price increases with each additional seat. The price is calculated based on:

```rust
pub fn get_place_buy_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
    let df = get_dec_factor(dec_factor);
    Ok(get_reserve(supply + 1, df)? - get_reserve(supply, df)?)
}

pub fn get_place_sell_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
    let df = get_dec_factor(dec_factor);
    Ok(get_reserve(supply, df)? - get_reserve(supply - 1, df)?)
}
```
The problem:
1. Between transaction submission and execution, other legitimate market transactions can change `perp_clients_count`, causing the actual execution price to differ from what the user expected
2. Users have no way to specify a maximum acceptable price for buying or minimum acceptable price for selling
3. The price is calculated and immediately applied without any validation against user expectations
4. During periods of high market activity, concurrent seat purchases/sales can cause significant price drift

**Impact:**
- **Unpredictable Execution:** Users have no guarantee that their transaction will execute at an acceptable price, even in normal market conditions
- **Poor User Experience:** Users cannot protect themselves from unfavorable price movements caused by legitimate concurrent market activity

**Recommended Mitigation:** Add slippage protection by allowing users to specify maximum/minimum acceptable prices in the instruction data, and validate the calculated price against these limits before execution.

**Deriverse:** Fixed in commit [a8181f3](https://github.com/deriverse/protocol-v1/commit/a8181f37e475eb1144f39490b62e45a476b2455d).

**Cyfrin:** Verified
