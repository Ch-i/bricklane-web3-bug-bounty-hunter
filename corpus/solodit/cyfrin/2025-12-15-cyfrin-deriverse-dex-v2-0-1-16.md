---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-16
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
title: Attacker can extract value by buying and selling the seat
vuln_class: []
---

# Attacker can extract value by buying and selling the seat

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Whenever a user buys a seat, they must pay `seat_price` in the currency token. The `seat_price` depends on the `perp_clients_count` at the time of purchase. If the `perp_clients_count` is higher, the user will pay more for the seat; if it is lower, the seat will cost less.

```rust
    pub fn get_place_buy_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
        let df = get_dec_factor(dec_factor);
        Ok(get_reserve(supply + 1, df)? - get_reserve(supply, df)?)
    }
```


The attacker can exploit this behavior and extract profit by creating a scenario where the user ends up paying a much higher seat price. For example, assuming a currency X with 6 decimals:

1. Initially, the `perp_clients_count` is 199,999.
2. The attacker buys 1,000 seats to profit later.
3. During user transaction, the `perp_clients_count` is 200,999, and the user pays a seat price of 26,030,289.
5. The attacker then sells the 1,000 seats and extracts a profit of 1,030,788.
6. If the attacker had not performed this attack, the user would have only needed to pay 24,999,501 for their seat.

No front-running is required. An attacker can pre-purchase seats and later sell them to extract the funds without using the instrument.



**Impact:** The attacker can extract user funds through this behavior, causing the user to pay more than expected.


**Recommended Mitigation:** Recommendation is to store the seat price the user originally paid and later when the user sells the seat return the exact same amount they paid at the time of purchase.

**Deriverse:** Fixed in commit [a80b0e](https://github.com/deriverse/protocol-v1/commit/a80b0ebf90f707d8e527cbcccce0790f35676d13).

**Cyfrin:** Verified.
