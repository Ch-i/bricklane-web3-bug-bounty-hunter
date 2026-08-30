---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Unsafe Arithmetic in `total_position_staked` Updates
vuln_class: []
---

# Unsafe Arithmetic in `total_position_staked` Updates

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** `clmm_lp_farming` program increases and decreases `total_positions_staked` by **1** in `stake_clmm_position` and `withdraw_clmm_position` functions respectively:
```rust
        ctx.accounts.farm.total_positions_staked += 1;
```
```rust
        ctx.accounts.farm.total_positions_staked -= 1;
```
Considering rust will wrap around and will allow overflows in release mode if not explicitly stated otherwise (by adding `overflow-checks = true` to `Cargo.toml`), these operations are not safe.

**Recommended Mitigation:** Consider using `checked_add()` and `checked_sub` functions to prevent overflows.

**Doryoku:**
Fixed in [fad227e](https://github.com/Warlands-Nft/belo_clmm_lp_farming/commit/fad227e80c53e207a8836365ed0c8449a17f2992).

**Cyfrin:** Verified.
