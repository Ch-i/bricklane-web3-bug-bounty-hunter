---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Dividend Calculation Uses Stale Token Balance in Subsequent `update()` Calls
  After `fees_deposit` with DRVS
vuln_class: []
---

# Dividend Calculation Uses Stale Token Balance in Subsequent `update()` Calls After `fees_deposit` with DRVS

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `fees_deposit()` function calls `client_community_state.update()` before `client_state.sub_crncy_tokens()`, causing `self.header.drvs_tokens` to be updated with a stale value that doesn't reflect the actual token balance after the reduction. When `update()` is called again in subsequent instructions (e.g., `deposit`, `spot_quotes_replace`), it calculates dividends using this stale stored value instead of the actual current balance.

**Prerequisites**: This issue only occurs when `fees_deposit` is called with `token_id = 0` (DRVS token)

The issue occurs because:

1. **Order of operations**: In `fees_deposit()`, `update()` is called before `sub_crncy_tokens()`
2. **Stale balance storage**: `update()` reads the current balance (before reduction) and stores it in `self.header.drvs_tokens`, but `sub_crncy_tokens()` reduces the actual balance afterward
3. **Stale dividend calculation**: When `update()` is called again in a subsequent instruction, it calculates dividends using `self.header.drvs_tokens` (the stale stored value from before the reduction) instead of the actual current balance

```rust
// src/program/processor/fees_deposit.rs
client_community_state.update(&mut client_state, &mut community_state)?;
client_state.resolve(AssetType::Token, data.token_id, TokenType::Crncy, false)?;
// ... fee calculation logic ...
client_state.sub_crncy_tokens(data.amount)?;
```

```rust
// src/state/client_community.rs
        if available_tokens != self.header.drvs_tokens {
            for (i, d) in self.data.iter_mut().enumerate() {
                let amount = (((community_state.base_crncy[i].rate - d.dividends_rate)
                    * self.header.drvs_tokens as f64) as i64)
                    .max(0);
                d.dividends_value += amount;
            }
```

**Example scenario demonstrating the issue:**

Initial state: User has 100 DRVS tokens, `self.header.drvs_tokens = 100`

1. **First `fees_deposit(token_id=0, amount=10)` call:**
   - `update()` is called:
     - `resolve(AssetType::Token, 0, ...)` resolves DRVS token (token_id = 0)
     - `available_tokens = 100` (current balance before reduction)
     - `self.header.drvs_tokens = 100` (stored value)
     - Since they're equal, no dividend calculation occurs
     - `self.header.drvs_tokens` is updated to `100`
   - `sub_crncy_tokens(10)` is called, actual balance becomes `90`
   - **Result**: `self.header.drvs_tokens = 100` (stale), but `actual balance = 90`

2. **Next instruction that calls `update()` (e.g., `deposit`, `spot_quotes_replace`):**
   - `update()` is called again:
     - `available_tokens = 90` (actual current balance, or could be others)
     - `self.header.drvs_tokens = 100` (stale stored value from step 1)
     - Since they differ, dividend calculation occurs using `self.header.drvs_tokens = 100`
     - **Problem**: Dividends are calculated based on `100` tokens, but the user only has `90` tokens during this period
   - **Result**: User receives dividends calculated on `100` tokens instead of `90`, receiving more than they should

The root cause is that in `fees_deposit()`, `update()` stores the balance before `sub_crncy_tokens()` reduces it, creating a discrepancy between the stored value and the actual balance. When `update()` is called again later, it uses this stale stored value for dividend calculations.

**Impact:** **Overpayment of Dividends**: When `update()` is called in subsequent instructions after a `fees_deposit(token_id=0)`, users receive dividends calculated on a higher token balance than they actually hold, leading to financial loss for the protocol.

**Recommended Mitigation:** The order should be re-arranged to ensure that the `drvs_token` is always update to date

**Deriverse:** Fixed in commit [4df80d](https://github.com/deriverse/protocol-v1/commit/4df80d97a4b72e144ccabf6956d10d463d4ca91e).

**Cyfrin:** Verified.
