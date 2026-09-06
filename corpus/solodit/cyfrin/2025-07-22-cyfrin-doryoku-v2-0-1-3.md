---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Steep Stepwise Jumps in Burn Percentages
vuln_class: []
---

# Steep Stepwise Jumps in Burn Percentages

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** `burn_pct` (burn percentage) does not utilize any precision multiplier and its value can be minimum **2** and maximum **50** with initial configuration. Calculation for `burn_pct` as follows:
```rust
            (state.min_burn_pct as u64)
                .saturating_sub(((over_min * burn_range) / time_range) as u64)
```
Changing these variables with their initial configuration, we can approximate the calculation with this formula:
```rust
    50 - 48 * ( (vest_duration - 10 days ) / 170 days )
```
This formula consists of steep stepwise jumps with every jump occurring approximately in **3.5 day** intervals.

Hence, the percentages of tokens that will be burned will be the same for a user who vests for *10 days* and the user who vests for *13.4 days*.

**Recommended Mitigation:** Introduce basis points (bips) or another high-precision scaler to burning percentage calculation to smoothen stepwise jumps. Example implementation with basis points:
```diff
-        state.min_burn_pct = 50; // 50% @ min
-        state.max_burn_pct = 2; //  2% @ max
+        state.min_burn_pct = 5_000; // 50% in basis points (bips) @ min
+        state.max_burn_pct = 200; //  2% in basis points (bips) @ max
```
```diff
        let burn_amount = amount
            .saturating_mul(burn_pct)
-            .checked_div(100)
+            .checked_div(10_000) // %100 in basis points (bips)
            .ok_or(ErrorCode::ArithmeticError)?;
```
**Doryoku:**
Fixed in [034eaac](https://github.com/Warlands-Nft/xbelo/commit/034eaac1863cd4e409b7777220a5e083bdbde030).

**Cyfrin:** Verified.


\clearpage
