---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-23-cyfrin-securitize-solana-vault-v2-0-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-23-cyfrin-securitize-solana-vault-v2-0
title: Lack of `mut` on `liquidation_token_mint` restricts redemption flexibility
vuln_class: []
---

# Lack of `mut` on `liquidation_token_mint` restricts redemption flexibility

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-23-cyfrin-securitize-solana-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md)_

---

**Description:** When firing `liquidate_handler` and the Vault is redepmtion vault. we provide the necessary liquidate account (mint, vault, token_program, ...). `liquidation_token_mint` is not market with `mut` flag.

> bc-solana-vault-sc/programs/sc-vault/src/instructions/liquidator/liquidate.rs#Liquidate
```rust
pub struct Liquidate<'info> {
    ...
    /// The mint account for the liquidation token.
    ///
    /// This account is only required when redemption program is enabled.
    /// It defines the liquidation tokens that will be received after redemption.
    #[account(
        mint::token_program = liquidation_token_program,
    )]
    pub liquidation_token_mint: Option<Box<InterfaceAccount<'info, Mint>>>,
    ...
}
```

This will prevent Redemption program to change the `mint` program. This will prevent the redemption program to mint `liquidation_amount` for example (if the program is the authority of liquidation token), as it will need to write to the account.

If the `redemption program` has the authority of `liquidation_token_mint` and it will work by taking `assets` and mint necessary `liquidation_tokens` it can't be done using the current interface. this affects the flexibility of the redemption programs to be introduced.

**Impact:**
- Preventing redemption program to supporting minting liquidation_token

**Recommended Mitigation:**
- Mark the account with `mut` in both `Liquidate` and `redemption_interface::Redeem`

**Securitize:** Fixed in [61d4f8c](https://github.com/securitize-io/bc-solana-vault-sc/commit/61d4f8c8958ab564a1153375e362b385df575fcf).

**Cyfrin:** Verified

\clearpage
