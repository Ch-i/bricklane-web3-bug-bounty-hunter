---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-merkle-airdrop-2-5
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-merkle-airdrop
title: '[I-06] Redundant check'
vuln_class: []
---

# [I-06] Redundant check

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Merkle-Airdrop.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md)_

---

**Files:** [claim.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/2025f68a4d699cc4997c133775f26f2768aba7e6/programs/merkle-token-distributor-solana/src/instructions/claim.rs#L126)

**Description:**

The claim instruction contain redundant checks for `fee_collector`. The `fee_collector` is checked in the ctx and then checked again in the execution logic.

```rust
/// CHECK: Checked in the function call.
#[account(constraint = fee_collector.key() == airdrop.fee_collector.key())]
pub fee_collector: UncheckedAccount<'info>,

// ...
pub fn claim(...) -> Result<()> {
    // Fee collector
    require!(
        ctx.accounts.unlocker.fee_collector == ctx.accounts.fee_collector.key(),
        TokenTableError::InvalidFeeCollector
    );
}
```

**Impact:** Redundant checks increase the execution overhead of the transaction call.

**Recommendation(s):** It is recommended to remove the redundant checks.

**Status:** Fixed

**Update from TokenTable:** Redundant checks removed in [1aed8dad5fca73dd7e7b3d2a666c939a39a37be6](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/1aed8dad5fca73dd7e7b3d2a666c939a39a37be6).
