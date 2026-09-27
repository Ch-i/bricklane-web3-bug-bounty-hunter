---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-2-3
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
title: SPL investor token account is not explicitly restricted to Token-2022
vuln_class: []
---

# SPL investor token account is not explicitly restricted to Token-2022

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** The SPL registration instruction constrains the mint and authority of `investor_token_account`, but
does not bind its owner to the instruction's fixed `Token2022` program:

```rust
#[account(
    token::mint = asset_mint,
    token::authority = investor_wallet,
)]
pub investor_token_account: Option<Box<InterfaceAccount<'info, TokenAccount>>>;
```

`anchor_spl::token_interface::TokenAccount` accepts accounts owned by either the legacy Token
program or Token-2022. Without `token::token_program = token_program`, Anchor therefore does not
check that this particular account is owned by Token-2022. The DS registration path includes that
constraint.

**Impact:** The practical impact is limited to clarity: the account definition is broader than intended and differs from the equivalent DS
definition.


**Recommended Mitigation:** Make the intended owner check explicit.

**Securitize**
Fixed in commit [f9a347b](https://github.com/securitize-io/bc-solana-whitelister/commit/f9a347bf15843343a093542ace1a4809514a30b5).

**Cyfrin:** Verified.
