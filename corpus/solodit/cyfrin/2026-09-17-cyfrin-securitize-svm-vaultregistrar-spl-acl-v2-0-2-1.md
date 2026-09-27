---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-2-1
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
title: Operators can thaw a frozen vault ATA through `register_vault_spl` under extreme
  cases
vuln_class: []
---

# Operators can thaw a frozen vault ATA through `register_vault_spl` under extreme cases

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** `register_vault_spl` is callable by any admin or operator (`is_authorized_caller`), and its `thaw_vault_token_account_if_frozen` invokes the same ACL `thaw_account` CPI signed by the `vault_registrar_authority` PDA whenever the vault token account is `AccountState::Frozen`. That thaw does not distinguish a freeze imposed by the mint's `DefaultAccountState` from a freeze applied by the token administrator to a specific account. The standalone `thaw_vault_token_account_spl` gates the identical call behind `has_one = admin`, but the registration path reaches the same thaw through a lower-privileged caller for a vault that has not yet been registered.

Also, `register_vault_spl` provides an operator-accessible route to the same sensitive thaw operation that `thaw_vault_token_account_spl` deliberately reserves for the registrar admin. Registration accepts an existing canonical vault ATA through `init_if_needed`. after creating a missing `InvestorRegistry`, it thaws that ATA whenever it is frozen. Consequently, if compliance administrators **freeze a vault and delete its registry as part of revocation**, an operator can select the same vault, recreate its registry from another investor record, and thaw the legally or administratively frozen ATA. The registration path contains no distinction between a newly default-frozen ATA and a previously existing externally frozen ATA.

```rust
/// Closes the registry account and refunds rent to `receiver` (or `signer` when
/// `receiver` is omitted). Callable by admin or by a freeze authority of the mint.
pub fn delete_investor_registry_handler(ctx: Context<DeleteInvestorRegistry>) -> Result<()> {
    if ctx.accounts.signer.key() != ctx.accounts.spl_whitelist_state.admin {
        require_freeze_authority(
            &ctx.accounts.signer,
            &ctx.accounts.mint.to_account_info(),
            &ctx.accounts.freeze_authority.to_account_info(),
            ctx.accounts.srfc37_authority.as_ref().map(|a| a.as_ref()),
            ctx.accounts.access_control_state.as_ref(),
        )?;
    }

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

**Impact:** The impact is limited. It's theoretically valid, but it has some strong prerequisites:

1. A vault account has been frozen and is not connected to any investor.
2. A vault account has been frozen and its registry has been revoked.

Both are strong prerequisites, so this is just as a reminder. As a result, an operator can register a not-yet-registered vault and, as a side effect, thaw its frozen associated token account, reversing a compliance or legal freeze that the registrar's own design scopes to the admin.

**Recommended Mitigation:** Either:
1. During the operation process, simply avoid making the vault account isolated (where it has not been connected to any investor).
2. Only permit the thaw from time-locks, with a strong validation.


**Securitize:** Fixed in commit: [80246a](https://github.com/securitize-io/bc-solana-whitelister/commit/80246acd05e0af91d329e7df0fe769aa4778c009)

**Cyfrin:** Verified.
