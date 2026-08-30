---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Initialization Allows Omitted `asset_vault` Although Swaps Require It
vuln_class: []
---

# Initialization Allows Omitted `asset_vault` Although Swaps Require It

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** `initialize` defines `asset_vault` as an optional account (`Option<Box<InterfaceAccount<TokenAccount>>>`) and uses `init_if_needed`. This permits creating on‑ramp instances without an asset_vault. However, swap instructions (`swap_spl_token`, `swap_ds_token`, `subscribe_ds_token`) require a non‑optional `asset_vault` account and will fail if it does not exist. This can lead to deployed on‑ramps that are unusable for swaps, especially for two‑step transfers.

```rust
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        mut,
        constraint = is_initializer_allowed(&admin.key())
            @ crate::errors::SecuritizeOnRampError::Forbidden,
    )]
    pub admin: Signer<'info>,

    #[account(
        mint::token_program = asset_token_program,
        mint::authority = asset_mint_authority,
    )]
    pub asset_mint: Box<InterfaceAccount<'info, Mint>>,
    /// CHECK: Mint authority for the asset mint
    pub asset_mint_authority: AccountInfo<'info>,

    #[account(
        init_if_needed,
        payer = admin,
        associated_token::mint = asset_mint,
        associated_token::authority = on_ramp_authority,
        associated_token::token_program = asset_token_program,
    )]
    pub asset_vault: Option<Box<InterfaceAccount<'info, TokenAccount>>>,
```

**Impact:** An on‑ramp can be initialized in a state that prevents swaps.

**Recommended Mitigation:** Make `asset_vault` a required account in the `initialize` instruction.

**Securitize:** Fixed in [e2807db](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/e2807db4f483cc3acf421f479248cf8f7acc66bd).

**Cyfrin:** Verified.
