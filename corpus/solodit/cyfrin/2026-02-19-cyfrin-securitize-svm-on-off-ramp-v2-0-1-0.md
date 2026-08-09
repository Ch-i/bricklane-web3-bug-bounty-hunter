---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Unvalidated Payer in DS Token Issue CPI Allows Protocol or Registrar to Pay
  Creation Fees
vuln_class: []
---

# Unvalidated Payer in DS Token Issue CPI Allows Protocol or Registrar to Pay Creation Fees

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** In `MintingAssetProvider::supply_to` (DsToken branch), the `payer` account for the `rwa_rbac::issue_tokens` CPI is taken directly from `additional_accounts[1]` with no validation against the intended fee payer.

```rust
                let rwa_rbac_program = &additional_accounts[0];
                let payer: &_ = &additional_accounts[1];
                let controller_authority = &additional_accounts[2];
                // ... other accounts ...
                rwa_rbac::cpi::issue_tokens(
                    CpiContext::new_with_signer(
                        rwa_rbac_program.to_account_info(),
                        rwa_rbac::cpi::accounts::IssueTokens {
                            payer: payer.to_account_info(),
                            user: authority.to_account_info(),
                            // ...
                        },
                        supply_signer,
                    ),
                    // ...
                )?
```


This allows:

1. **PDA drain**: In `swap_ds_token` (and operator swap), the caller can set `payer` to the `on_ramp_authority` PDA. The PDA already signs via `supply_signer`; if it holds any lamports (e.g. accidental deposit or future design change), those lamports can be used to pay for token account creation and other CPI fees, effectively draining protocol-held funds.
2. **Registrar pays instead of investor**: The protocol does **not** validate that the payer is the investor. In `subscribe_ds_token`, the user supplies `asset_provider_accounts` via `remaining_accounts`. The user can set `asset_provider_accounts[1]` (the payer) to `registrar_authority`. Because `registrar_authority` is a `Signer` in the instruction, the `rwa_rbac::issue_tokens` CPI will accept them as payer and the **protocol (registrar)** will pay for the investor’s token account creation (e.g. `init_if_needed`). This violates the intended design that the **user (investor)** should pay for their own account creation; the protocol is made to bear the cost.


The downstream `rwa_rbac::issue_tokens` logic typically uses `payer` for account creation (e.g. `init_if_needed` with `payer = payer`). Whoever is placed in `payer` therefore pays rent/creation; with no validation, that can be the `on_ramp PDA` or the `registrar` instead of the investor.
```rust
#[account(
        init_if_needed,
        payer = payer,
        associated_token::token_program = token_program,
        associated_token::mint = asset_mint,
        associated_token::authority = to,
    )]
    pub token_account: Box<InterfaceAccount<'info, TokenAccount>>,
```

**Impact:**
- **On-ramp authority PDA**: If the PDA ever holds lamports (e.g. mistaken transfer, future feature), any user calling `swap_ds_token` (or operator swap) can set `payer` to the PDA and cause those lamports to be spent on issue_tokens fees (e.g. token account creation). Impact is limited today if the PDA is not expected to hold balance but is a real risk if the design or usage changes.
- **Registrar as payer**: Because the payer is not validated, a user can set it to `registrar_authority` in `subscribe_ds_token` and force the protocol to pay for the investor’s token account creation. This is a direct economic cost to the protocol, contradicts the intended “user pays” design, and can be abused (e.g. high subscription volume) to shift creation costs to the protocol.


**Recommended Mitigation:** Make sure the `payer` is the `invester`.

**Securitize:** Fixed in [4382392](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/438239289ef5427a4f5158c92b2c477193e92bf2).

**Cyfrin:** Verified.

\clearpage
