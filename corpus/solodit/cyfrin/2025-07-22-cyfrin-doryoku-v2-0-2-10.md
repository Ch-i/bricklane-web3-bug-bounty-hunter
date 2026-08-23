---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-10
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Unutilized `position_collection` Field in Events
vuln_class: []
---

# Unutilized `position_collection` Field in Events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** When a user stakes and withdraws, `CLMMPositionStaked` and `CLMMPositionWithdrawn` events are emitted respectively.
Both of these events include a `Pubkey` field named `position_collection`.
However in both actions, that field is emitted as `Pubkey::default()`:
```rust
        emit!(CLMMPositionStaked {
            user: user_stake.user,
            position_mint: ctx.accounts.position_mint.key(),
            clmm_pool: ctx.accounts.farm.clmm_pool,
            duration_months,
            start_time: user_stake.start_ts,
            end_time: user_stake.start_ts + user_stake.duration,
            position_collection: Pubkey::default(),
        });
```
Hence it is not used.


**Recommended Mitigation:** Consider removing the `position_collection` field from `CLMMPositionStaked` and `CLMMPositionWithdrawn` events if it has not have a functionality in off-chain system.

**Doryoku:**
Fixed in [fad227e](https://github.com/Warlands-Nft/belo_clmm_lp_farming/commit/fad227e80c53e207a8836365ed0c8449a17f2992).

**Cyfrin:** Verified.

\clearpage
