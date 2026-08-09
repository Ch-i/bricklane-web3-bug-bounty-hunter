---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-22
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
title: Users incur losses when selling seats
vuln_class: []
---

# Users incur losses when selling seats

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Whenever a user buys or sells a seat, we calculate the seat price at that moment using the difference between `get_reserve` from the new/current position and the old position.
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
The `get_reserve` function returns an i64, whose maximum value is 9223372036854775807. and, in `get_reserve` calculation is done in f64 and if the result in f64 exceeds this limit, casting it back to i64 will clamp the value to the maximum i64 value (9223372036854775807).

Example: The seat price from 249,995 to 250,000, the value becomes zero when `crncy_token_decs_count` is 9.


**Impact:** This leads to unexpected behavior, which can result in losses for regular users and create opportunities for an attacker to extract value if `perp_clients_count` is close 250000.



**Recommended Mitigation:** `get_reserve` should return f64. After computing the difference between the results of both `get_reserve` calls, we can then convert the final value back to i64 for more accurate result.

**Deriverse:** Fixed in commit [c8d26d](https://github.com/deriverse/protocol-v1/commit/c8d26d57c1d9f24add2ed449f422d79ec983c13a).

**Cyfrin:** Verified.
