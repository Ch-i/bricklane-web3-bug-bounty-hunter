---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-23-cyfrin-securitize-solana-vault-v2-0-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-23-cyfrin-securitize-solana-vault-v2-0
title: Redundant `vault_authority_signer` passed to `BurnChecked` in `redeem` and
  `liquidate`
vuln_class: []
---

# Redundant `vault_authority_signer` passed to `BurnChecked` in `redeem` and `liquidate`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-23-cyfrin-securitize-solana-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md)_

---

**Description:** Both `redeem_handler` and `liquidate_handler` build their burn CPI like this:

```rust
let burn_ctx = CpiContext::new_with_signer(
    ctx.accounts.share_token_program.to_account_info(),
    BurnChecked {
        mint: ctx.accounts.share_mint.to_account_info(),
        from: ctx.accounts.<share_ata>.to_account_info(),
        authority: ctx.accounts.<operator_or_liquidator>.to_account_info(),
    },
    vault_authority_signer,              // ← unnecessary
);
burn_checked(burn_ctx, shares, ctx.accounts.share_mint.decimals)?;
```

The SPL-Token program requires **only the `authority` account to sign**.
Here the authority is the operator/liquidator, who is already a transaction-signer.
Adding `vault_authority_signer`:

* Produces an extra PDA signature that the token program ignores.
* Consumes compute units each time the instruction runs.


**Recommended Mitigation:** * Build the burn context without extra signers:

  ```rust
  let burn_ctx = CpiContext::new(
      ctx.accounts.share_token_program.to_account_info(),
      BurnChecked {
          mint: ctx.accounts.share_mint.to_account_info(),
          from: ctx.accounts.<share_ata>.to_account_info(),
          authority: ctx.accounts.<operator_or_liquidator>.to_account_info(),
      },
  );
  ```

* Keep `vault_authority_signer` only for calls that truly need the PDA to sign (e.g., vault asset transfers).
This removes superfluous signatures, lowers compute costs, and avoids accidental brittleness.

**Securitize:** Fixed in [3635c15](https://github.com/securitize-io/bc-solana-vault-sc/commit/3635c15d920a3f40f75604e2bff4872f2e3f091e).

**Cyfrin:** Verified
