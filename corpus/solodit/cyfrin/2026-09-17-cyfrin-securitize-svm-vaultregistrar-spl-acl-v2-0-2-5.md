---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-2-5
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
title: '`VaultRegistrarInitialized` omits the initial `require_investor_signature`
  value'
vuln_class: []
---

# `VaultRegistrarInitialized` omits the initial `require_investor_signature` value

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** During initialization, `require_investor_signature` is correctly stored in the registrar state:
```rust
let state = VaultRegistrarState {
    // ...
    require_investor_signature,
    // ...
};
```
However, the emitted `VaultRegistrarInitialized` event does not include this value:
```rust
pub struct VaultRegistrarInitialized {
    pub registrar: Pubkey,
    pub id: u64,
    pub admin: Pubkey,
    pub asset_mint: Pubkey,
    pub token_config: TokenConfig,
    // Missing require_investor_signature
}
```
By contrast, later updates include the value in `RequireInvestorSignatureUpdated`:
```rust
emit!(RequireInvestorSignatureUpdated {
    registrar: state.key(),
    admin: ctx.accounts.admin.key(),
    require_investor_signature,
});
```

**Recommended Mitigation:** Add `require_investor_signature` to `VaultRegistrarInitialized` and include it when emitting the event:
```rust
pub struct VaultRegistrarInitialized {
    pub registrar: Pubkey,
    pub id: u64,
    pub admin: Pubkey,
    pub asset_mint: Pubkey,
    pub token_config: TokenConfig,
    pub require_investor_signature: bool,
}
```

**Securitize:** Fixed in commit [c481756](https://github.com/securitize-io/bc-solana-whitelister/commit/c4817565a20f0e2812cab6313f69c165dee62a8e).

**Cyfrin:** Verified.

\clearpage
