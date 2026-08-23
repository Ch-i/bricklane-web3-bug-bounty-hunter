---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-18
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
title: Using a stale `perp_price_delta` to calculate the `perp_funding_rate`
vuln_class: []
---

# Using a stale `perp_price_delta` to calculate the `perp_funding_rate`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The funding rate is calculated using `change_funding_rate`, but this function computes `perp_funding_rate` based on the previous `perp_price_delta`, which is outdated.

```rust
    pub fn change_funding_rate(&mut self) {
        let time_delta = self.time - self.state.header.perp_funding_rate_time;
        if time_delta > 0 && self.state.header.perp_price_delta != 0.0 {
            self.state.header.perp_funding_rate +=
                ((time_delta as f64) / DAY as f64) * self.state.header.perp_price_delta;
        }
        self.state.header.perp_price_delta =
            (self.market_px() - self.state.header.perp_underlying_px) as f64 * self.rdf;
        self.state.header.perp_funding_rate_time = self.time;
    }
```
This can result in losses for some users and unintended profits for others, depending on whether the market price is below or above the underlying price.

Scenario:


1. The market price and the underlying price of Bitcoin are both 100k.
2. Alice opens a 1× long position for 1 BTC at 100k, and Bob opens a 1 BTC short position at the same price.
3. After one day, the underlying price of Bitcoin increases from 100k to 110k, but the market price remains unchanged.
4. When Alice and Bob attempt to close their positions after one day, the funding rate is calculated using the old delta.
5. As a result, Alice receives no funding payment even though the difference between the market price and underlying price is now 10k, and Bob does not pay any funding despite being on the paying side.

The funding rate is intended to ensure that the market price tracks the underlying price. Calculating the funding rate using an old delta fails to create this corrective force.

**Impact:** The funding rate is being calculated using a stale delta, users may end up receiving or paying funding later than they should. This can lead to unintended losses or profits depending on when a user enters or exits a position, as shown in the scenario above.

**Recommended Mitigation:** To mitigate this, `change_funding_rate` should first calculate the updated delta and then compute the funding rate based on that value.
```rust
    pub fn change_funding_rate(&mut self) {
        let time_delta = self.time - self.state.header.perp_funding_rate_time;
        self.state.header.perp_price_delta =
            (self.market_px() - self.state.header.perp_underlying_px) as f64 * self.rdf;
        if time_delta > 0 && self.state.header.perp_price_delta != 0.0 {
            self.state.header.perp_funding_rate +=
                ((time_delta as f64) / DAY as f64) * self.state.header.perp_price_delta;
        }
        self.state.header.perp_price_delta =
            (self.market_px() - self.state.header.perp_underlying_px) as f64 * self.rdf;
        self.state.header.perp_funding_rate_time = self.time;
    }
```
**Deriverse:** Acknowledged; we think our approach is better as in a scenario where the price delta was unchanged most of the time between perp transactions our approach is more relevant.
