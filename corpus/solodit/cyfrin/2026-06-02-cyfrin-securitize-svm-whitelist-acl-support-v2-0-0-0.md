---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0
title: '`spl_token_whitelist::change_admin` is single-step and accepts any `Pubkey`
  including the default zero key'
vuln_class: []
---

# `spl_token_whitelist::change_admin` is single-step and accepts any `Pubkey` including the default zero key

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md)_

---

**Description:** `change_admin_handler` writes the caller-supplied `new_admin` into `SplWhitelistState::admin` after only checking `state.admin != new_admin`. There is no `require_keys_neq!(new_admin, Pubkey::default(), ...)` filter, no validation that `new_admin` is a Signer in the same transaction, and no two-step propose-then-accept handshake. Because every other admin-gated instruction (`pause`, `unpause`, future `change_admin`) is bound by `has_one = admin`, a rotation to the all-zero pubkey or to any address whose private key is not held by the protocol team permanently locks those instructions - no further signer can satisfy `has_one = admin`, and the upgrade authority is not re-consulted after `initialize`.
```rust
/// Updates the admin pubkey stored in the whitelist state.
pub fn change_admin_handler(ctx: Context<ChangeAdmin>, new_admin: Pubkey) -> Result<()> {
    let spl_whitelist_state = &mut ctx.accounts.spl_whitelist_state;

    require!(
        spl_whitelist_state.admin != new_admin,
        SplWhitelistErrorCode::NoChange
    );

    spl_whitelist_state.admin = new_admin;

    emit!(crate::events::AdminChanged {
        admin: ctx.accounts.admin.key(),
        new_admin,
    });

    Ok(())
}
```

The same shape exists in the `dstoken-whitelist` program's `change_admin` handler (out of formal audit scope; included for context - the mitigation should be applied symmetrically across both programs).

**Impact:** If the admin signs a `change_admin` instruction with `new_admin = Pubkey::default()` (a fat-finger encoding mistake, an SDK / CLI argument-construction bug, a JSON deserialization that defaults missing fields to zero) or with any address whose key the team cannot produce on a later signature, the whitelist state PDA becomes administratively bricked. `pause` and `unpause` can no longer be called, so the only operational kill-switch protecting the permissionless `whitelist` instruction is lost. A subsequent `change_admin` to recover from the mistake is also blocked, since the current `admin` field is unsignable. The only remaining recovery is a program redeploy by the upgrade authority that rewrites `change_admin_handler` (or that re-initializes the state PDA through a migration). The harm requires admin error or key compromise to manifest, which caps severity at Low, but recovery is non-trivial and operationally disruptive.

**Recommended Mitigation:** Add a zero-key filter and adopt a two-step rotation in both `change_admin` handlers. Concretely, in `programs/spl-token-whitelist/src/instructions/admin/change_admin.rs` (and apply the same change symmetrically to the `dstoken-whitelist` `change_admin` handler, which is out of formal audit scope):

1. Reject the default pubkey at the top of the handler:

```rust
require_keys_neq!(
    new_admin,
    Pubkey::default(),
    SplWhitelistErrorCode::InvalidAdmin
);
```

2. Split the rotation into a propose step (the current admin writes the proposed admin key into a new pending-admin field on the state PDA) and an accept step that requires the new admin to sign the second transaction and clears the pending-admin field upon acceptance. This guarantees that the destination key is controlled by a live signer before it replaces the active admin. If the propose/accept refactor is out of scope for this release, at minimum require the `new_admin` to sign the same `change_admin` transaction by adding a second `Signer<'info>` account to the `ChangeAdmin` struct and constraining it so that the signer's key equals `new_admin`.

**Securitize:** Acknowledged.

\clearpage
