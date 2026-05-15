---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Inconsistent Price Calculation for Fee in Spot LP Trading
vuln_class: []
---

# Inconsistent Price Calculation for Fee in Spot LP Trading

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The fee calculation in the `spot_lp` instruction uses `last_px` directly without applying the same price constraints (`best_bid, best_ask`) and unit conversion (`RDF`) that are used when adding liquidity. This inconsistency can lead to incorrect fee calculations when `last_px` falls outside the valid market price range.

In `src/program/processor/spot_lp.rs`, there are two different price calculation approaches:

1. When adding liquidity:

```rust
let px_f64 = instr_state
    .header
    .last_px
    .max(instr_state.header.best_bid)
    .min(instr_state.header.best_ask) as f64
    * RDF;
```

This calculation constrains the price to the range `[best_bid, best_ask]`

2. When calculating fees

```rust
fees = 1
    + ((instr_state.header.last_px as f64
        / get_dec_factor(instr_state.header.asset_token_decs_count) as f64)
        as i64)
        .max(1);
```

Uses `last_px` directly without price range constraints.

**Impact:** If `last_px` is outside `[best_bid, best_ask]` (e.g., due to market volatility or order book changes), fees may be calculated using an invalid price, leading to overcharging or undercharging users.

**Recommended Mitigation:** Update the fee calculation to use the same price logic as liquidity addition:


**Deriverse:** Fixed in commit [40e36f70](https://github.com/deriverse/protocol-v1/commit/40e36f70a57a89a76ec19f9d825852bced7002dd).

**Cyfrin:** Verified.
