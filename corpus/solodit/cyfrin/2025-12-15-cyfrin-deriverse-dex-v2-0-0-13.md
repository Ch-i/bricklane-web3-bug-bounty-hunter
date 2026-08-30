---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-13
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Shorts can withdraw full available funds instead of being restricted to margin
  call limits in `perp-withdraw`
vuln_class: []
---

# Shorts can withdraw full available funds instead of being restricted to margin call limits in `perp-withdraw`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In [perp_withdraw.rs](https://github.com/deriverse/protocol-v1/blob/f611019674f668681c3dbe074f8b7bc2ba846c97/src/program/processor/perp_withdraw.rs#L99), the margin call detection logic fails to detect for shorts ,where [is_long_margin_call()](https://github.com/deriverse/protocol-v1/blob/f611019674f668681c3dbe074f8b7bc2ba846c97/src/program/processor/perp_withdraw.rs#L147) is called twice instead of checking both long and short positions:
```rust
        engine.check_long_margin_call()?;
        engine.check_short_margin_call()?;
        //@audit both are long, one should be short
        let margin_call = engine.is_long_margin_call() || engine.is_long_margin_call();
        if !margin_call {
            engine.check_rebalancing()?;
}
```
When a user has a short perpetual position that is in margin call (underwater/undercollateralized), the `margin_call` variable incorrectly evaluates to false because:
- `is_long_margin_call()` returns `false` for short positions
- The duplicate call also returns `false`
- Result: [margin_call = false || false = false]

**Impact:**
1. Bypassed Withdrawal Restrictions
The withdrawal amount calculation differs based on margin call status:
```rust
let amount = if margin_call {
    // Limited withdrawal - only excess margin above requirements
    let margin_call_funds = funds.min(engine.get_avail_funds(client_state.temp_client_id, true)?);
    if margin_call_funds <= 0 {
        bail!(ImpossibleToWithdrawFundsDuringMarginCall);
    }
    // Restricted amount
} else if data.amount == 0 {
    funds  // Full funds available - NO RESTRICTIONS
} else {
    // Normal withdrawal
};
```
This lets users with underwater short positions withdraw full available funds instead of being restricted to margin call limits. This allows extraction of collateral that should be locked to cover their short position's potential losses.

2. Incorrect Rebalancing Execution
When `margin_call` is incorrectly `false` for short positions in margin call, `check_rebalancing()`is called when it shouldn't be..

**Recommended Mitigation:** Replace current condition to this:
```rust
let margin_call = engine.is_long_margin_call() || engine.is_short_margin_call();
```
**Deriverse:** Fixed in commit: https://github.com/deriverse/protocol-v1/commit/4f7bc8ac68325aa93b339ff91c0ac794ea17ffd9

**Cyfrin:** Verified.
