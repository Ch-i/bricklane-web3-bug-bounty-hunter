---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-0-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: De-whitelisting closes `InvestorRegistry` but does not re-freeze the owner's
  token accounts
vuln_class: []
---

# De-whitelisting closes `InvestorRegistry` but does not re-freeze the owner's token accounts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** The SPL whitelist program provides a single onboarding path (`whitelist`) that both provisions the per-`(mint, owner)` `InvestorRegistry` and thaws the owner's frozen Token-2022 accounts. The only reverse path exposed by the program is `delete_investor_registry`, which closes the registry PDA but leaves the owner's ATA(s) thawed. A wallet that has been removed from compliance metadata can therefore continue to send and receive tokens on Solana, even though cross-chain bridging is blocked by the missing registry.


Onboarding is fully handled inside `whitelist`:

```51:126:bc-solana-whitelist-sc/programs/spl-token-whitelist/src/instructions/whitelist.rs
/// Thaws each remaining account after validating ownership and mint/freeze authority,
/// then provisions the `(mint, owner)` `InvestorRegistry` if it does not exist yet.
pub fn whitelist_handler<'info>(
    mut ctx: Context<'_, '_, '_, 'info, Whitelist<'info>>,
    investor_id: String,
) -> Result<()> {
    // ...
    let registry_created = ensure_investor_registry(&mut ctx, &investor_id)?;
    // ...
    // Thaw the token accounts
    for token_account_info in token_accounts_infos.iter() {
        // ...
        require!(
            token_account.state
                == anchor_spl::token_2022::spl_token_2022::state::AccountState::Frozen,
            SplWhitelistErrorCode::AccountNotFrozen
        );

        freeze_authority_type.thaw_account(/* ... */)?;
    }
    // ...
}
```

The reverse operation only closes the registry account and refunds rent. It performs no token-account state change:

```59:86:bc-solana-whitelist-sc/programs/spl-token-whitelist/src/instructions/admin/delete_investor_registry.rs
/// Closes the registry account and refunds rent to `receiver` (or `signer` when
/// `receiver` is omitted). Callable by admin or by a freeze authority of the mint.
pub fn delete_investor_registry_handler(ctx: Context<DeleteInvestorRegistry>) -> Result<()> {
    // ... authorization ...
    emit!(crate::events::InvestorRegistryDeleted {
        mint: ctx.accounts.investor_registry.mint,
        wallet: ctx.accounts.investor_registry.wallet,
    });

    let rent_receiver = ctx
        .accounts
        .receiver
        .as_ref()
        .map(|r| r.to_account_info())
        .unwrap_or_else(|| ctx.accounts.signer.to_account_info());

    ctx.accounts.investor_registry.close(rent_receiver)?;

    Ok(())
}
```

There is no symmetric `unwhitelist` / `delist` instruction in the program that accepts the owner's token accounts and CPIs into ACL/`token_2022::freeze_account`.

**Impact:** Operators may treat registry deletion as complete de-whitelisting, while cross-chain blocking and on-chain transfer blocking diverge. Cross-chain is disabled but on-chain transfers are not.


**Recommended Mitigation:** Add a symmetric offboarding path that mirrors `whitelist`.

**Securitize:** Acknowledged as by design. The program-level asymmetry doesn't cause the described divergence because freezing is intentionally decoupled from registry management and handled off-chain by our trusted backend.

\clearpage
