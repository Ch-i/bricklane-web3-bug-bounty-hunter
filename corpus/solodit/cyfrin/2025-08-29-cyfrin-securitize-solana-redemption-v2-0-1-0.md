---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-securitize-solana-redemption-v2-0-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-securitize-solana-redemption-v2-0
title: DoS in initialize via pre-created ATA for `off_ramp_authority`
vuln_class: []
---

# DoS in initialize via pre-created ATA for `off_ramp_authority`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md)_

---

**Description:** The `initialize` instruction creates the liquidity vault as an **associated token account** for the program PDA `off_ramp_authority`:
```rust
#[account(
    init,
    payer = admin,
    associated_token::mint = liquidity_token_mint,
    associated_token::authority = off_ramp_authority,
    associated_token::token_program = liquidity_token_program,
)]
pub liquidity_token_vault: Box<InterfaceAccount<'info, TokenAccount>>;
```
Associated token accounts are globally derivable and can be created by **anyone** for any owner without the owner’s signature. Because both `off_ramp_state` and `off_ramp_authority` PDAs are deterministically derived from public seeds (counter and state key), an attacker can precompute the vault ATA and create it first. When `initialize` later runs with `init`, Anchor will fail with “already in use,” reverting the whole transaction.

**Impact:** Hard denial of service on program initialization for a given `(off_ramp_state, liquidity_token_mint)`. An attacker can repeatedly grief by precreating the ATA for each anticipated off_ramp ID, blocking deployment unless the admin changes parameters. This is cheap for the attacker and can be repeated.

**Recommended Mitigation:** Switch to `init_if_needed` to make initialization idempotent and immune to precreation:
```rust
#[account(
    init_if_needed,
    payer = admin,
    associated_token::mint = liquidity_token_mint,
    associated_token::authority = off_ramp_authority,
    associated_token::token_program = liquidity_token_program,
)]
pub liquidity_token_vault: Box<InterfaceAccount<'info, TokenAccount>>;
```
This accepts a pre-existing correct ATA and proceeds.


**Securitize:** Fixed in [1a8a098](https://github.com/securitize-io/bc-solana-redemption-sc/commit/1a8a0989c940eb8978ff3556bfc513ee0606f6dc).

**Cyfrin:** Verified.
