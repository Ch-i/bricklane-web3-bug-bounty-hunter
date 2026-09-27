---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: Unprivileged pre-funding of the registrar authority PDA can cause a retry-stable
  denial of SPL vault registration
vuln_class: []
---

# Unprivileged pre-funding of the registrar authority PDA can cause a retry-stable denial of SPL vault registration

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** Note:  SPL only. `register_vault_ds` does not call `fund_authority_for_rent` or use the registrar authority PDA as a rent payer; it forwards the transaction payer directly to the DS CPI. Therefore, the pre-funded PDA residue mechanism described below does not affect DS registration.

 Affected path: SPL only. register_vault_ds does not call fund_authority_for_rent or use
  the registrar authority PDA as a rent payer; it forwards the transaction payer directly to
  the DS CPI. Therefore, the pre-funded PDA residue mechanism described below does not
  affect DS registration.

`register_vault_spl` uses the System-owned `vault_registrar_authority` PDA as both signer and rent payer for the whitelist CPI that creates a vault's `InvestorRegistry`. Immediately before the CPI, `fund_authority_for_rent` tops the PDA up to the expected account-creation rent:

```rust
fn fund_authority_for_rent(ctx: &Context<RegisterVaultSpl>) -> Result<()> {
    let authority = ctx.accounts.vault_registrar_authority.to_account_info();

    let required = Rent::get()?.minimum_balance(INVESTOR_REGISTRY_ACCOUNT_LEN);
    let shortfall = required.saturating_sub(authority.lamports());

    if shortfall == 0 {
        return Ok(());
    }

    let cpi_accounts = Transfer {
        from: ctx.accounts.payer.to_account_info(),
        to: authority,
    };

    transfer(
        CpiContext::new(ctx.accounts.system_program.to_account_info(), cpi_accounts),
        shortfall,
    )
}
```

The calculation assumes the PDA begins at or below `required`, but its address is publicly derivable and anyone can transfer lamports to it. An attacker can pre-fund it with `required + 1`; `saturating_sub` then returns zero, so the registrar performs no top-up. If `spl_token_whitelist::create_investor_registry` debits the full fresh-account rent, the PDA is left with one lamport:

```text
pre-CPI authority balance  = required + 1
registrar top-up           = 0
whitelist account rent     = required
post-CPI authority balance = 1
```

Because the authority is writable, System-owned, and has zero data, it begins the registration rent-exempt but would finish rent-paying. Agave rejects this `RentExempt -> RentPaying` transition with `InsufficientFundsForRent`. The transaction rolls back and restores the `required + 1` balance, so ordinary retries fail identically until another transfer moves the PDA outside the rent-paying residue band.

The registrar arithmetic and Agave v3.1.3 rent rule are verified. The remaining dependency gate is the locked private whitelist: final confirmation requires establishing that deployed `create_investor_registry` uses the authority as payer and debits the full fresh-account rent. The local interface and documentation say `signer` is the payer, but do not verify the unavailable implementation's internal behavior.

**Impact:** Any funded account can temporarily block all new `register_vault_spl` operations for a targeted registrar. While the PDA remains in the poisoned range, new vaults cannot obtain their compliance registry; on default-frozen mints, they also cannot complete the create-and-thaw onboarding flow.

Recovery is permissionless. For the `required + 1` trigger, adding `Rent::minimum_balance(0) - 1` lamports makes the post-CPI balance exactly `Rent::minimum_balance(0)`, allowing the authority to remain rent-exempt and registration to complete.

The registrar is therefore not permanently bricked, and a correctly diagnosed top-up restores service cheaply. However, ordinary retries do not self-heal, the runtime error does not identify the poisoned PDA, and an attacker can repeatedly re-arm public registrar authorities.

**Recommended Mitigation:** Ensure the authority's post-CPI balance is always either zero or rent-exempt. Possible approaches include:

- After the whitelist CPI, use the registrar authority seeds to transfer any residual lamports back to the transaction payer, leaving the authority at zero before transaction-level rent validation.
- Before the CPI, normalize an externally funded balance and then fund exactly the amount the CPI will debit.
- If a residual must remain, top the authority up so its expected post-CPI balance is at least `Rent::minimum_balance(0)` rather than inside the rent-paying interval.
- Preferably, update the whitelist interface to separate authorization from payment so the transaction payer funds `InvestorRegistry` creation directly and the authority PDA never acts as a rent transit account.

**Securitize:** Fixed in commit [17eedbb](https://github.com/securitize-io/bc-solana-whitelister/commit/17eedbb9f40e3db86d2ec901687dcb883af47ff7).

**Cyfrin:** Verified.
