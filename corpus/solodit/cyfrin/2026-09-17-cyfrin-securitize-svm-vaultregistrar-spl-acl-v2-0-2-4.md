---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-2-4
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: '`VaultRegisteredDs` can report a signer unrelated to the attached identity'
vuln_class: []
---

# `VaultRegisteredDs` can report a signer unrelated to the attached identity

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** Note: This is found during the path comparison between DS and SPL token.

`existing_investor_wallet` remains an `Option<Signer>` even when `require_investor_signature` is disabled. The constraints that link this signer to the required `identity_account` are declared on the optional `existing_investor_wallet_identity` account. Anchor evaluates those constraints only when that account is provided, so omitting it skips both the `has_one = identity_account` check and the wallet-key match.

```rust
    pub existing_investor_wallet: Option<Signer<'info>>,

    #[account(
        has_one = identity_account @ VaultRegistrarError::IdentityNotOwnedByInvestor,
        constraint = existing_investor_wallet.as_ref().is_none_or(|wallet| {
            wallet.key() != ZERO_PUBKEY
        }) @ VaultRegistrarError::InvalidAddress,
        constraint = existing_investor_wallet.as_ref().is_none_or(|wallet| {
            existing_investor_wallet_identity.wallet == wallet.key()
        }) @ VaultRegistrarError::IdentityNotOwnedByInvestor,
    )]
    pub existing_investor_wallet_identity: Option<Account<'info, WalletIdentity>>,

```

The optional `investor_token_account` likewise constrains mint and authority only when present. Even then it binds the token account to `existing_investor_wallet`, not to `identity_account`.

The handler requires all three investor accounts only when `require_investor_signature` is enabled. With the flag disabled, an authorized operator can supply signer `B` as `existing_investor_wallet`, omit the identity and token accounts, and still attach the vault to an unrelated but otherwise valid `identity_account` `A`.

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

The RWA-RBAC CPI uses the required `identity_account` and does not consume `existing_investor_wallet`. The event independently populates `investor` from `existing_investor_wallet`, so its attribution can disagree with the identity actually attached to the vault.

```rust
    emit!(VaultRegisteredDs {
        registrar: ctx.accounts.vault_registrar_state.key(),
        caller: ctx.accounts.caller.key(),
        vault: ctx.accounts.vault_wallet.key(),
        asset_mint: ctx.accounts.asset_mint.key(),
        identity_account: ctx.accounts.identity_account.key(),
        investor: ctx
            .accounts
            .existing_investor_wallet
            .as_ref()
            .map(|w| w.key()),
    });
```

1. Create a DS registrar with `require_investor_signature = false`.
2. As an authorized operator, call `register_vault_ds` with valid accounts for identity `A` and:
   - `existing_investor_wallet = B`, where `B` signs the transaction (the operator itself can be
     used);
   - `existing_investor_wallet_identity = None`;
   - `investor_token_account = None`.
3. The vault is attached to identity `A`. `VaultRegisteredDs` reports `investor = Some(B)`.

**Impact:** The event's `investor` field cannot reliably identify the investor associated with `identity_account` when signature enforcement is disabled. It also should not be treated as proof that the attached investor consented to the registration. Under the current trust model, it works well, but the team should be notified about this condition.


**Recommended Mitigation:** Emit `investor = None` when `require_investor_signature` is disabled. Alternatively, if partial investor accounts are not intended, reject them and emit the signer only after validating its `WalletIdentity` against `identity_account`.

**Securitize:** Fixed in commit [47c4f8](https://github.com/securitize-io/bc-solana-whitelister/commit/47c4f8bfe635dbe6ef8b090795afbf562bc0a51e).

**Cyfrin:** Verified.
