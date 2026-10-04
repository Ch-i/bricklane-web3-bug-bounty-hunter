---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-0-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: Frozen investors can still pass the participation gate and register a new vault
vuln_class: []
---

# Frozen investors can still pass the participation gate and register a new vault

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** When `require_investor_signature` is on, both `register_vault_spl` and `register_vault_ds` require the investor to sign and to present a token account with `amount > 0`. Neither path reads `state`.

SPL (`require_investor_participation`):

```rust
fn require_investor_participation(ctx: &Context<RegisterVaultSpl>) -> Result<()> {
    if !ctx
        .accounts
        .vault_registrar_state
        .require_investor_signature
    {
        return Ok(());
    }

    require!(
        ctx.accounts.investor_wallet.to_account_info().is_signer,
        VaultRegistrarError::InvestorAccountsRequired
    );

    let investor_token_account = ctx
        .accounts
        .investor_token_account
        .as_ref()
        .ok_or(VaultRegistrarError::InvestorAccountsRequired)?;

    require!(
        investor_token_account.amount > 0,
        VaultRegistrarError::InvestorHasNoBalance
    );

    Ok(())
}
```

DS (`register_vault_ds`):

```rust
if vault_registrar_state.require_investor_signature {
    require!(
        ctx.accounts.existing_investor_wallet.is_some()
            && ctx.accounts.existing_investor_wallet_identity.is_some()
            && ctx.accounts.investor_token_account.is_some(),
        VaultRegistrarError::InvestorAccountsRequired
    );

    let investor_token_account = ctx.accounts.investor_token_account.as_ref().unwrap();

    require!(
        investor_token_account.amount > 0,
        VaultRegistrarError::InvestorHasNoBalance
    );
}
```

Freezing a Token/Token-2022 account does not clear its balance, so a legitimately frozen investor ATA still passes. After that:

- SPL copies `investor_id` into a new vault registry and thaws the new vault ATA when the mint uses `DefaultAccountState` (new accounts start frozen):

```rust
if ctx.accounts.vault_token_account.state != AccountState::Frozen {
    return Ok(());
}

cpi::acl::thaw_account::handler(
    &ctx.accounts.acl_thaw_accounts,
    ctx.accounts.vault_registrar_authority.to_account_info(),
    ctx.accounts.asset_mint.to_account_info(),
    ctx.accounts.vault_token_account.to_account_info(),
    ctx.accounts.token_program.to_account_info(),
    state.id,
    state.authority_bump,
)?;
```

**Impact:** The freeze stays on the original account. Those tokens still cannot move. What the investor gets is a new path: the SPL vault ATA is usable, or the DS wallet is newly attached, and future tokens can land there.

**Recommended Mitigation:** Reject `investor_token_account.state == Frozen` (require `Initialized`) in both registration paths.

**Securitize:** Fixed in commit [dc71c35](https://github.com/securitize-io/bc-solana-whitelister/commit/dc71c35ef8c3feba15283d151a617d1fc36ce78a).

**Cyfrin:** Verified.
