---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-merkle-airdrop-2-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-merkle-airdrop
title: '[I-01] Allow the fee_collector to be set arbitrarily during the initialization
  of the airdrop account'
vuln_class: []
---

# [I-01] Allow the fee_collector to be set arbitrarily during the initialization of the airdrop account

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Merkle-Airdrop.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md)_

---

**Files:** [initialize.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/merkle-token-distributor-solana/src/instructions/initialize.rs)

**Description:**

In the `initialize` instruction, if `init_fee_account` is set to `false`, then the check `ctx.accounts.fee_collector.as_ref().unwrap().key() == fee_collector.key()` is skipped. This means that it allows the `airdrop.owner` to initialize any `fee_collector`.

```rust
pub fn initialize(...) -> Result<()> {
    ctx.accounts.airdrop.owner = owner;
    ctx.accounts.airdrop.fee_collector = fee_collector;
    ctx.accounts.airdrop.project_token = project_token;

    if init_fee_account {
        // Before we init the fee account, ensure we are calling the expected fee_collector program from
        // the parameters and that all required accounts are provided.
        require!(
            ctx.accounts.fee_collector.is_some() &&
                ctx.accounts.fee.is_some() &&
                ctx.accounts.fee_collector_storage.is_some() &&
                ctx.accounts.fee_collector.as_ref().unwrap().key() == fee_collector.key(),
            TokenTableError::InvalidFeeCollector
        );
        //...
    }
}
```

**Impact:** In the current system, allowing the `fee_collector` account to be set arbitrarily during initialization does not cause any loss, because the no-fee claim, as designed by the protocol, fails due to a constraint in the ctx. However, the `airdrop.owner` may have the motivation to initialize the `fee_collector` as `pubkey::default` during initialization. This would enable claims related to that account to be processed without any fees.

**Recommendation(s):** It is recommended not to allow the `airdrop.owner` to arbitrarily initialize the `fee_collector`.

**Status:** Fixed

**Update from TokenTable:** In [aa48e8ab3c30b65f0e90a3be35cdb81a7f7f9461](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/aa48e8ab3c30b65f0e90a3be35cdb81a7f7f9461), `fee_collector` program account verification is handled manually. Anchor now expects an `UncheckedAccount<>`, and in all instructions where `fee_collector` can be set, we verify that the provided account matches the instruction parameter value and that the provided account is executable.
