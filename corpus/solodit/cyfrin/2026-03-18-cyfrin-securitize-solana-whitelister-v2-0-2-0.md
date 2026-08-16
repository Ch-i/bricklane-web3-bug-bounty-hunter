---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-18-cyfrin-securitize-solana-whitelister-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-18-cyfrin-securitize-solana-whitelister-v2-0
title: '`VaultRegistered` event omits investor signer when signature is required'
vuln_class: []
---

# `VaultRegistered` event omits investor signer when signature is required

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md)_

---

**Description:** The `VaultRegistered` event at `register_vault.rs:138-144` emits `registrar`, `caller`, `vault`, `asset_mint`, and `identity_account`, but does not include the `existing_investor_wallet` pubkey when `require_investor_signature` is enabled.

```rust
emit!(VaultRegistered {
    registrar: ctx.accounts.vault_registrar_state.key(),
    caller: ctx.accounts.caller.key(),
    vault: ctx.accounts.vault_wallet.key(),
    asset_mint: ctx.accounts.asset_mint.key(),
    identity_account: ctx.accounts.identity_account.key(),
});
```

Off-chain monitoring systems cannot determine which investor provided consent from the event alone.

**Recommended Mitigation:** Add an optional `investor` field to the `VaultRegistered` event.

**Securitize:** Fixed in [17bb95e](https://github.com/securitize-io/bc-solana-whitelister/commit/17bb95e22b0d4130753c4d37ed1f9596c7f21f0e).

**Cyfrin:** Verified.
