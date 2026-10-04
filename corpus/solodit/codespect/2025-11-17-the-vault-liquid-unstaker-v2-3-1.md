---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-11-17-the-vault-liquid-unstaker-v2-3-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md
tags:
- firm:codespect
- report:2025-11-17-the-vault-liquid-unstaker-v2
title: '[L-02] The liquid_unstake_lst(...) and liquid_unstake_lst_wrapped(...) instructions
  lack address verification.'
vuln_class: []
---

# [L-02] The liquid_unstake_lst(...) and liquid_unstake_lst_wrapped(...) instructions lack address verification.

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-11-17-The-Vault-Liquid-Unstaker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md)_

---

**Files:** [`liquid_unstake_lst.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/dba32c9fce1310b23f9d1a5a0407602bcd7446b7/programs/liquid-unstaker/src/instructions/liquid_unstake_lst.rs#L217), [`liquid_unstake_lst_wrapped.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/dba32c9fce1310b23f9d1a5a0407602bcd7446b7/programs/liquid-unstaker/src/instructions/liquid_unstake_lst_wrapped.rs#L218)

**Description:**

In the `liquid_unstake_lst(...)` and `liquid_unstake_lst_wrapped(...)` instructions, a `stake_account_info` account is created. The expected account address is `b"stake_account_info"`, a PDA derived using `destination_stake_accounts` as the seed. However, there is no account address verification, which allows a malicious actor to provide any signed address to be created as `stake_account_info` instead of the intended address.

```rust
let create_stake_account_info_instruction = solana_program::system_instruction::create_account(
    &ctx.accounts.payer.key(),
    &stake_info_accounts[i].key(),
    stake_info_rent,
    8 + StakeAccountInfo::LEN as u64,
    &ctx.program_id
);
let (_, bump) = Pubkey::find_program_address(&[b"stake_account_info", destination_stake_acccounts[i].key.as_ref()],
    &crate::id());

solana_program::program::invoke_signed(
    &create_stake_account_info_instruction,
    &[
        ctx.accounts.payer.to_account_info(),
        stake_info_accounts[i].to_account_info(),
        ctx.accounts.system_program.to_account_info(),
    ],
    &[&[b"stake_account_info", destination_stake_acccounts[i].key.as_ref(), &[bump]]],
)?;
```

**Impact:** If the above situation occurs, the `withdraw_stake_account(...)` instruction will fail due to seed mismatch, but the funds can still eventually be released to the vault via the `update(...)` instruction.

**Recommendation:** It is recommended to verify that the `stake_info_accounts` passed in match the expected addresses.

```diff
- let (_, bump) = Pubkey::find_program_address(&[b"stake_account_info",
-     destination_stake_acccounts[i].key.as_ref()], &crate::id());
+ let (expect_address, bump) = Pubkey::find_program_address(&[b"stake_account_info",
+     destination_stake_acccounts[i].key.as_ref()], &crate::id());
+ if stake_info_accounts[i].key != expected_address {
+     return Err(ProgramError::InvalidAccountData);
+ }
```

**Status:** Fixed

**Update from The Vault:** Resolved in [d9b62dc9c110a2f8693e000ce2eb51dff5c45430](https://github.com/SolanaVault/liquid-unstaker/commit/d9b62dc9c110a2f8693e000ce2eb51dff5c45430).
