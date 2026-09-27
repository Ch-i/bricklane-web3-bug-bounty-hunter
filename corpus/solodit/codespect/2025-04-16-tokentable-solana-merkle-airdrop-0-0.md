---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-merkle-airdrop-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-merkle-airdrop
title: '[M-01] The set_default_fee_collector instruction cannot be executed'
vuln_class: []
---

# [M-01] The set_default_fee_collector instruction cannot be executed

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Merkle-Airdrop.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md)_

---

**Files:** [set_fee_collector.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/2025f68a4d699cc4997c133775f26f2768aba7e6/programs/merkle-token-distributor-solana/src/instructions/set_default_fee_collector.rs)

**Description:**

The `set_default_fee_collector` instruction is used to modify the `default_fee_collector`. Since it requires `config.admin` for permission validation, the config account should have already been initialized when calling the instruction. However, due to the incorrect assignment of the `init` attribute to the config account in the ctx, the `set_default_fee_collector` instruction fails to execute successfully.

```rust
#[derive(Accounts)]
#[instruction(_default_fee_collector: Pubkey)]
pub struct SetDefaultFeeCollector<'info> {
    #[account(
        init,
        seeds = [b"config".as_ref()],
        bump,
        payer = authority,
        space = 8 + Config::INIT_SPACE
    )]
    pub config: Account<'info, Config>,
    //...
}
```

**Impact:** The `default_fee_collector` cannot be successfully set.

**Recommendation(s):** It is recommended to remove the `init` attribute from the config account in the ctx.

**Status:** Fixed

**Update from TokenTable:** Removed `init` attribute from the config account in the Anchor context in [e2cf5fbc8802845c56d0e0ab48c874c0000ce015](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/e2cf5fbc8802845c56d0e0ab48c874c0000ce015) and added `mut` attribute in [8edb2ab7e2a63c37258b78f365bce2d43db3403f](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/8edb2ab7e2a63c37258b78f365bce2d43db3403f).
