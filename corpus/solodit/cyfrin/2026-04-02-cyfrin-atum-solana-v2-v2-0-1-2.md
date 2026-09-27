---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-02-cyfrin-atum-solana-v2-v2-0-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-04-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-02-cyfrin-atum-solana-v2-v2-0
title: '`Fulfillment` Proxy Does Not Support Token-2022 TransferHook Extension'
vuln_class: []
---

# `Fulfillment` Proxy Does Not Support Token-2022 TransferHook Extension

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-02-cyfrin-atum-solana-v2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md)_

---

**Description:** The escrow program correctly forwards `remaining_accounts` in all token transfer CPI calls:

```rust
    token::transfer_checked(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            TransferChecked {
                from: ctx.accounts.authority_ata.to_account_info(),
                to: ctx.accounts.escrow_ata.to_account_info(),
                authority: ctx.accounts.escrow_delegate.to_account_info(),
                mint: ctx.accounts.mint.to_account_info(),
            },
            signer_seeds,
        )
        .with_remaining_accounts(ctx.remaining_accounts.to_vec()),
        amount,
        decimals,
    )?;
```

The same pattern is used in `release`and `refund`.

The `fulfillment_proxy` program performs token transfers **without** forwarding `remaining_accounts`:

```rust
    token::transfer_checked(
        CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            TransferChecked {
                from: ctx.accounts.from_ata.to_account_info(),
                to: ctx.accounts.to_ata.to_account_info(),
                authority: ctx.accounts.settler.to_account_info(),
                mint: ctx.accounts.mint.to_account_info(),
            },
        ),
        amount,
        ctx.accounts.mint.decimals,
    )?;
```

The `strict_fulfill` instruction (lines 61–74) has the same omission. Even if the client passes TransferHook accounts as remaining accounts, they are ignored because the program does not call `.with_remaining_accounts(ctx.remaining_accounts.to_vec())`.

**Impact:**
- Users cannot fulfill payments using Token-2022 tokens with TransferHook. The transfer CPI will fail.
- Escrow supports `TransferHook` but `fulfillment_proxy` does not.

**Recommended Mitigation:** Add `.with_remaining_accounts(ctx.remaining_accounts.to_vec())` to `transfer_checked` CPI calls.

**Atum:** Fixed in [b4c128e](https://github.com/Atum-Labs/solana-escrow/commit/b4c128e78d8b91112a242b652cfb8b8f4ee0e736).

**Cyfrin:** Verified.

\clearpage
