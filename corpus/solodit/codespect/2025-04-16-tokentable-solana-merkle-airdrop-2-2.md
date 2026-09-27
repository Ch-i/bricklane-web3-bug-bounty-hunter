---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-merkle-airdrop-2-2
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
title: '[I-03] Lack of Option wrapper on fee account'
vuln_class: []
---

# [I-03] Lack of Option wrapper on fee account

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Merkle-Airdrop.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md)_

---

**Files:** [claim.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/merkle-token-distributor-solana/src/instructions/claim.rs#L133)

**Description:**

The claim instructions are invoked with a few accounts related to fee collection:

- `authority_fee_ata`;
- `fee_collector_storage`;
- `fee_collector_vault`;
- `fee_collector`;
- `fee_token_mint`;
- `fee`;
- `fee_token_program`;

The fee collection mechanism is optional, hence the design allows skipping them if they are unnecessary through the `Option` wrapper on the account type in the instructions contexts.

The fee account however is not:

```rust
/// CHECK: The account is checked in the FeeCollector, not here.
#[account(mut)]
pub fee: UncheckedAccount<'info>,
```

**Impact:** Expected difficulties in building the fee-less transactions as the fee account still needs to be provided to the instruction call.

**Recommendation(s):** Wrap the fee account type in `Option`.

**Status:** Fixed

**Update from TokenTable:** As of [78051afb53579a4e6558519000d6c35f510a5533](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/78051afb53579a4e6558519000d6c35f510a5533), the fee collection mechanism is no longer optional. `fee` is a required account and the documented structure here is needed to support the updated fee collection mechanism.
