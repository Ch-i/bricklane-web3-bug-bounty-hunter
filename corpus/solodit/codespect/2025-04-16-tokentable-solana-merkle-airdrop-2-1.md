---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-merkle-airdrop-2-1
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
title: '[I-02] Changing the fee_collector to a different program will cause instructions
  to fail'
vuln_class: []
---

# [I-02] Changing the fee_collector to a different program will cause instructions to fail

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Merkle-Airdrop.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md)_

---

**Files:** [set_fee_collector.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/merkle-token-distributor-solana/src/instructions/set_fee_collector.rs)

**Description:**

The `set_fee_collector` instruction allows setting a different `fee_collector` program for Airdrop’s fee processing capabilities, as per TokenTable’s feedback from the previous audit:

The problem arises when the `FeeCollector` `program_id` is changed and certain instructions which take the `fee_collector` program account are called. The Anchor implementation under the hood will validate the program account against the `program_id` of the `FeeCollector` which was placed there at compile time:

```rust
pub fee_collector: Option<Program<'info, FeeCollector>>,
```

**Impact:** It will not be possible to update the `fee_collector` program account without also updating the entire merkle token distributor program.

**Recommendation(s):** Remove the `fee_collector` account from Anchor’s context structs and handle it manually within the instruction code.

**Status:** Fixed

**Update from TokenTable:** In [aa48e8ab3c30b65f0e90a3be35cdb81a7f7f9461](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/aa48e8ab3c30b65f0e90a3be35cdb81a7f7f9461), `fee_collector` program account verification is handled manually. Anchor now expects an `UncheckedAccount<>`, and in all instructions where `fee_collector` is used, we verify that the provided account matches the expected unlocker’s/airdrop’s `fee_collector` but skip the account executable check, since this would have already been checked when the account was set.
