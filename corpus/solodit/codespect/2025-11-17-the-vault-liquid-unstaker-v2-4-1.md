---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-11-17-the-vault-liquid-unstaker-v2-4-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md
tags:
- firm:codespect
- report:2025-11-17-the-vault-liquid-unstaker-v2
title: '[I-02] Some instructions could be DoS due to account creation failure'
vuln_class: []
---

# [I-02] Some instructions could be DoS due to account creation failure

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-11-17-The-Vault-Liquid-Unstaker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md)_

---

**Files:** [`withdraw_stake_account.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/2dd71f5e3d9017504783c67bc1b903ecaa169a54/programs/liquid-unstaker/src/instructions/withdraw_stake_account.rs), [`liquid_unstake_lst_wrapped.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/2dd71f5e3d9017504783c67bc1b903ecaa169a54/programs/liquid-unstaker/src/instructions/liquid_unstake_lst_wrapped.rs), [`liquid_unstake_lst.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/2dd71f5e3d9017504783c67bc1b903ecaa169a54/programs/liquid-unstaker/src/instructions/liquid_unstake_lst.rs)

**Description:**

Some instructions need to create new accounts during execution, and due to improper checks, they could be DoS’ed. In the `liquid_unstake_lst_wrapped(...)` and `withdraw_stake_account(...)` instructions, when creating a `stake_account`, the account creation is skipped as long as the target account’s lamports are not 0. A malicious actor can front-run by depositing some lamports into the account, causing the instruction to fail.

```rust
// Create the destination stake account if not created already (paid by user)
if ctx.accounts.stake_account_destination.lamports() == 0 {

    let rent = rent.minimum_balance(solana_program::stake::state::StakeStateV2::size_of());

    let create_stake_account_info_instruction = solana_program::system_instruction::create_account(
        &ctx.accounts.user.key(),
        &ctx.accounts.stake_account_destination.key(),
        rent,
        solana_program::stake::state::StakeStateV2::size_of() as u64,
        &solana_program::stake::program::id()
    );
    //...
}
```

In the `liquid_unstake_lst_wrapped(...)` and `liquid_unstake_lst(...)` instructions, `stake_account_info` is created using `create_account`. Since the `create_account` instruction fails if the target account already has lamports, a malicious actor can front-run by depositing some lamports into the account, causing the `create_account` call to fail.

```rust
// Create the stake account info account
let stake_info_rent = Rent::get()?.minimum_balance(8 + StakeAccountInfo::LEN);
accumulated_rent_pda_accounts += stake_info_rent;

let create_stake_account_info_instruction = solana_program::system_instruction::create_account(
    &ctx.accounts.payer.key(),
    &stake_info_accounts[i].key(),
    stake_info_rent,
    8 + StakeAccountInfo::LEN as u64,
    &ctx.program_id
);
```

**Impact:** Some instruction calls could be DoS if a malicious actor donates lamports.

**Recommendation:** When checking whether an account needs to be created, verify not only whether lamports exist but also whether the account data size matches the expected size. When creating the account, call `create_account` only if lamports are 0; if not, top up the missing rent and then use `system_instruction::allocate` and `system_instruction::assign` to create the account.

**Status:** Fixed

**Update from The Vault:** Resolved in [7f5463199bc1da21df0f9e232e39502b10f4cfeb](https://github.com/SolanaVault/liquid-unstaker/commit/7f5463199bc1da21df0f9e232e39502b10f4cfeb).
