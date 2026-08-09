---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-27
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
title: User's chosen leverage is overwritten to `max-leverage` on every perp operation
vuln_class: []
---

# User's chosen leverage is overwritten to `max-leverage` on every perp operation

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In `client_primary.rs]`, the [new_for_perp](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/state/client_primary.rs#L344) function unconditionally sets the user's leverage on every call, regardless of whether the `alloc` parameter is true or false.
```rust
    let mut client_state = ClientPrimaryState::new_for_perp(
        program_id,
        client_primary_acc,
        &ctx,
        signer,
        system_program,
        0, //always passed as zero
        false,
        true,
    )?;
```
When [leverage = 0](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/state/client_primary.rs#L470) is passed (which happens in most perp operations like `perp_withdraw`, `perp_deposit`, `perp_mass_cancel`, `perp_order_cancel`, `perp_quotes_replace`, `perp_statistics_reset`, `buy_market_seat`, `sell_market_seat`), the code sets the user's leverage to `max_leverage`.

```rust
if leverage > 0 {
    //clear and set
    unsafe {
        (*state.perp_info2).mask &= 0xFFFFFF00;
        (*state.perp_info2).mask |= (leverage as u32).min(header.max_leverage as u32);
    }
} else {
    // When leverage == 0, sets to max_leverage (always by default)
    unsafe {
        (*state.perp_info2).mask &= 0xFFFFFF00;
        (*state.perp_info2).mask |= header.max_leverage as u32;
    }
}
Ok(state)
```
consider this scenario:
1. User calls perp_change_leverage(5) to set their leverage to 5x
   - leverage stored as 5

2. User calls `perp_deposit()` to add more margin
   - `new_for_perp()` called with leverage=0
   - leverage RESET to `max_leverage` (e.g., 15x)

3. User now has 15x leverage instead of 5x

**Impact:** Users who carefully set their leverage to a conservative value (e.g., 2x or 3x) will have it silently reset to `max_leverage` after performing any perp operation. This significantly increases their liquidation risk without their knowledge.

**Recommended Mitigation:** Only update leverage when explicitly requested (i.e., when `leverage > 0`). Remove the else branch that overwrites leverage with `max_leverage`:
```rust
if leverage > 0 {
    // Only update leverage when explicitly provided
    unsafe {
        (*state.perp_info2).mask &= 0xFFFFFF00;
        (*state.perp_info2).mask |= (leverage as u32).min(header.max_leverage as u32);
    }
}
// When leverage == 0, keep existing leverage unchanged
```
**Deriverse:** Fixed in commit: https://github.com/deriverse/protocol-v1/commit/e15ad9372bf10322c6d05c234189576b8aad3690

**Cyfrin:** Verified.
