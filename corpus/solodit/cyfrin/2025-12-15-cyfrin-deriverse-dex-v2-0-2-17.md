---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-17
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Silent Failure in `voting_reset`
vuln_class: []
---

# Silent Failure in `voting_reset`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `voting_reset` function silently ignores failures when attempting to upgrade the community account header for writing. If the `community_acc` account is not marked as writable, the `upgrade()` call fails, but the function still returns `Ok(())`, giving the caller a false impression that the voting parameters were successfully reset when they were not.

The voting_reset function uses if let `Ok(header) = community_state.header.upgrade()` to conditionally update the community account header. However, this pattern silently returns error that occurs when the account is not marked as writable.

```rust
    if let Ok(header) = community_state.header.upgrade() {
        header.spot_fee_rate = START_SPOT_FEE_RATE;
        header.perp_fee_rate = START_PERP_FEE_RATE;
        header.max_discount = START_MAX_DISCOUNT;
        header.margin_call_penalty_rate = START_MARGIN_CALL_PENALTY_RATE;
        header.fees_prepayment_for_max_discount = START_FEES_PREPAYMENT_FOR_MAX_DISCOUNT;
        header.spot_pool_ratio = START_SPOT_POOL_RATIO;
    }
```

Throughout the codebase, all other functions that use `upgrade` properly propagate errors using the `?` operator:

```rust
    if let Some(ref mut header) = client_state.header {
        header.upgrade()?.points = 0;
        header.upgrade()?.mask &= 0xFFFFFFFFFFFFFF;
    }
```

```rust
        if community_state.header.voting_counter == 0 {
            community_state.header.upgrade()?.voting_counter += 1;
        }
```

**Impact:** If the `community_acc` account is incorrectly not marked as writable (due to a bug in the caller or a configuration error), the function will appear to succeed but no state updates will occur.

**Recommended Mitigation:** Change the code to properly propagate the error when `upgrade()` fails.

**Deriverse:** Fixed in commit [9ef2d7](https://github.com/deriverse/protocol-v1/commit/9ef2d7602f2964b210e36b8d1de3360992d9caa2).

**Cyfrin:** Verified.

\clearpage
