---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Improper Rounding in Burn Logic Lets Users Avoid Penalty
vuln_class: []
---

# Improper Rounding in Burn Logic Lets Users Avoid Penalty

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** Vesting can happen with any positive value, it doesn't have a minimum value requirement as long as it is positive.
The amount that will be burned is currently configured to be in between 2% and 50% according to vesting time.
`burn_amount` is calculated as:
```rust
        let burn_amount = amount
            .saturating_mul(burn_pct)
            .checked_div(100)
            .ok_or(ErrorCode::ArithmeticError)?;
```
Here, `amount` represents the exact amount user is vesting, while `burn_pct` represents the burn percentage, and it's value will always be in between **2** and **50**.
Considering the burned amount will be calculated with `amount` multiplied by a value that is lower than **100**, and then it will be divided to **100**, this value will be rounding down.
While it is always optimal to round up fee/burn related values and this implementation breaks that, it also creates an opportunity to game the program to get rid of burning altogether.

Here is an example scenario that shows the impact:
- Alice vests **49** token with maximum vest time, hence burn_pct became **2**.
- This results with burn_amount that is equal to **0**.
- Alice vested without burning and can repeat this without any limit.

**Impact:** While the material impact is very limited, it let users vest without burning anything.
Calculation also leads to underestimation of burn amount by **1** for every vest.

**Recommended Mitigation:** Consider adding **1** to the `burn_amount` after the division is performed:
```diff
        let burn_amount: u64 = amount
            .saturating_mul(burn_pct)
+           .checked_add(99)
+           .ok_or(ErrorCode::ArithmeticError)?;
            .checked_div(100)
            .ok_or(ErrorCode::ArithmeticError)?;
```
**Doryoku:**
Fixed in [2a4e99c](https://github.com/Warlands-Nft/xbelo/commit/2a4e99cda5c5be1fae8f68023b7ec197a3229fc7).

**Cyfrin:** Verified.
