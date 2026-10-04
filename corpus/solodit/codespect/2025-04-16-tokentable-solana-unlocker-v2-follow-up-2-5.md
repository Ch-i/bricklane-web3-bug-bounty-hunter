---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-unlocker-v2-follow-up-2-5
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-unlocker-v2-follow-up
title: '[I-06] Redundant check'
vuln_class: []
---

# [I-06] Redundant check

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md)_

---

**Files:** [claim.rs](https://github.com/CODESPECT-security/011-TokenTable-Solana-UnlockerV2-FollowUp-Merkle/blob/2025f68a4d699cc4997c133775f26f2768aba7e6/programs/unlocker-v2-solana/src/instructions/claim.rs#L285), [claim_cancelled_actual_tokens.rs](https://github.com/CODESPECT-security/011-TokenTable-Solana-UnlockerV2-FollowUp-Merkle/blob/2025f68a4d699cc4997c133775f26f2768aba7e6/programs/unlocker-v2-solana/src/instructions/claim_cancelled_actual_tokens.rs#L184)

**Description:**

The `claim` and `claim_cancelled_actual_tokens` instructions contain redundant checks for `fee_collector`. The `fee_collector` is checked in the `ctx` and then checked again in the execution logic.

```rust
/// CHECK: Checked in the function call.
#[account(constraint = fee_collector.key() == airdrop.fee_collector.key())]
pub fee_collector: UncheckedAccount<'info>,

// ...

pub fn claim_cancelled_actual_tokens(...) -> Result<()> {
    // Fee collector
    require!(
        ctx.accounts.unlocker.fee_collector == ctx.accounts.fee_collector.key(),
        TokenTableError::InvalidFeeCollector
    );

pub fn claim(...) -> Result<()> {
    // Fee collector
    require!(
        ctx.accounts.unlocker.fee_collector == ctx.accounts.fee_collector.key(),
        TokenTableError::InvalidFeeCollector
    );
```

**Impact:** Redundant checks increase the execution overhead of the transaction call.

**Recommendation:** It is recommended to remove the redundant checks.

**Status:** Fixed

**Update from TokenTable:** Redundant checks removed in [1aed8dad5fca73dd7e7b3d2a666c939a39a37be6](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/1aed8dad5fca73dd7e7b3d2a666c939a39a37be6).
