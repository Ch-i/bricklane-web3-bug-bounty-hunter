---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-11
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: '`get_place_buy_price` function does not currently support the maximum `MAX_SUPPLY`
  value.'
vuln_class: []
---

# `get_place_buy_price` function does not currently support the maximum `MAX_SUPPLY` value.

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Whenever a user buys or sells a seat, we calculate the seat price at that moment using the difference between get_reserve from the new/current position and the old position.

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
In `get_reserve`, we calculate `difference_to_max`, which can become zero when the user is at the 250,000th position. As a result, the `reserve` becomes infinite, causing `get_reserve` to return i64::MAX.

```rust
pub fn get_reserve(supply: u32, dec_factor: i64) -> Result<i64, DeriverseError> {
    let difference_to_max = MAX_SUPPLY - supply as i64;
    if difference_to_max < 0 {
        bail!(InvalidSupply {
            supply,
            supply_difference: difference_to_max as u32
        });
    }

    let reserve = MAX_SUPPLY as f64 * INIT_SEAT_PRICE * supply as f64 / difference_to_max as f64;

    return Ok((reserve * dec_factor as f64) as i64);
}
```

**Impact:** A user buying at the 250,000th position will end up paying significantly more than a user buying at the 249,999th position, because `get_reserve` for supply + 1 returns i64::MAX.

**Recommended Mitigation:** When calculating `difference_to_max` for the last user, we should add +1 to ensure that the reserve does not become infinite.

**Deriverse:** Fixed in commit [c8d26d](https://github.com/deriverse/protocol-v1/commit/c8d26d57c1d9f24add2ed449f422d79ec983c13a).

**Cyfrin:** Verified.
