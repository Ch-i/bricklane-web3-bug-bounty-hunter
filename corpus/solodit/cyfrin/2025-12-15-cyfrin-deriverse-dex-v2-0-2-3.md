---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-3
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
title: Inflexible Voting System Prevents Rapid Parameter Adjustments
vuln_class: []
---

# Inflexible Voting System Prevents Rapid Parameter Adjustments

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The governance voting system uses a rigid rotation mechanism where which parameter can be modified is determined by `voting_counter % 6`.

This creates a fixed 6-parameter rotation cycle where each parameter can only be voted on once every 6 voting periods. Combined with the 14-day voting period duration, this means a specific parameter can only be modified again after approximately 84 days (6 periods × 14 days), severely limiting the protocol's ability to respond to urgent situations or make consecutive adjustments to the same parameter.

The parameter selection is determined in `finalize_voting()`:

```rust
let tag = community_account_header.voting_counter % 6;
match tag {
    0 => spot_fee_rate,
    1 => perp_fee_rate,
    2 => spot_pool_ratio,
    3 => margin_call_penalty_rate,
    4 => fees_prepayment_for_max_discount,
    _ => max_discount,
}
```

The `voting_counter` can only increment by 1 in `finalize_voting()`:

```rust
community_account_header.voting_counter += 1;
```

And in `next_voting()`, the counter can only be incremented to 1 if it's 0, or finalized (which increments by 1):

```rust
if community_state.header.voting_counter == 0 {
    community_state.header.upgrade()?.voting_counter += 1;
}
community_state.finalize_voting(clock.unix_timestamp as u32, clock.slot as u32)?;
```

**The Problem:**
1. There is no mechanism to skip voting rounds or target a specific parameter directly
2. The `voting_counter` can only increment sequentially, never skip ahead
3. If a parameter needs urgent adjustment or consecutive modifications, the protocol must wait through the entire 6-parameter cycle
4. No emergency mechanism exists for operator or admin to override the rotation schedule

**Example Scenario:**
1. Voting period 1 (`voting_counter` = 1): Community votes to decrease `perp_fee_rate` (tag `1`)
2. After 14 days, the change is applied, `voting_counter` becomes 2
3. Market conditions change, requiring another immediate adjustment to `perp_fee_rate`
4. The protocol must wait for voting_counter = `7, 13, 19`, etc. (every 6th period)
5. This means waiting approximately `70 days` (5 more periods × 14 days) before `perp_fee_rate` can be voted on again

```rust
#[cfg(not(feature = "test-sbf"))]
pub fn voting_end(time: u32) -> u32 {
    let days = (time - SETTLEMENT) / DAY;
    days * DAY + 14 * DAY + SETTLEMENT
}

```

**Impact:**
- **Delayed Response to Market Conditions:** The protocol cannot quickly respond to urgent situations requiring consecutive parameter adjustments
- **Inefficient Governance:** If a parameter needs multiple adjustments to reach an optimal value, the process takes months(5*14 = 70 days) instead of weeks

**Recommended Mitigation:** Consider adding an optional mechanism to allow the operator to specify the next `voting_counter` value in extreme circumstances, while maintaining the default sequential increment for normal operations.

**Deriverse::**
Fixed in commit [bb853ad](https://github.com/deriverse/protocol-v1/commit/bb853adf0cfecf974b1b1933a6192b4dfb7e42ae).

**Cyfrin:** Verified.
