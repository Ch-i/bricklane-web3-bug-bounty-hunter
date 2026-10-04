---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-atum-solana-v2-0-3-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-atum-solana-v2-0
title: refund can return assets to different Token Account that the one used for depositing
vuln_class: []
---

# refund can return assets to different Token Account that the one used for depositing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-atum-solana-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md)_

---

**Description:** When creating a delegation the depositor is enforced to use the ATA account and not any Token account, in depositing tokens for getting it back in different chain.

[escrow.rs#L33-L42](https://github.com/Atum-Labs/solana-escrow/blob/main/programs/escrow/src/instructions/escrow.rs#L33-L42)
```rust
pub struct Deposit<'info> {
    ...
    #[account(
        init_if_needed,
        payer = payer,
        associated_token::mint = mint,
        associated_token::authority = authority,
        associated_token::token_program = token_program,
        constraint = authority_ata.owner == authority.key() @ ErrorCode::InvalidAuthority,
        constraint = authority_ata.mint == mint.key() @ ErrorCode::InvalidData,
    )]
>>  pub authority_ata: InterfaceAccount<'info, TokenAccount>,
    ...
}
```

In case the Bridging process failed for any reason we transfer the funds back to the depositor. But the `depositor_ata` account is not enforced to be the ATA account, it can be any token account passed, we are just checking for authority and mint.

[escrow.rs#L122-L127](https://github.com/Atum-Labs/solana-escrow/blob/main/programs/escrow/src/instructions/escrow.rs#L122-L127)
```rust
pub struct Refund<'info> {
    ...
    #[account(
        mut,
        constraint = depositor_ata.owner == deposit.depositor @ ErrorCode::InvalidAuthority,
        constraint = depositor_ata.mint == deposit.mint @ ErrorCode::InvalidData,
    )]
>>  pub depositor_ata: InterfaceAccount<'info, TokenAccount>,
    ...
}
```

Because of this, the refunding process can end up of transfering tokens to different Token Account than the actual one paid for it

The same situation also exists in release function, where the receiver of the funds can't restrict the funds to an exact Token account, this can't be an issue as its own and can be by design, but in refund the funds can be paid by an account and refunded to another one, which should not occur in traditional financial systems.

**Impact:**
- The recipient Token Account of the refunded amount can differ from that original payer for it

**Recommended Mitigation:** We should make sure the `depositor` account passed is the ATA account, so that we guarantee the funds returned to the original payer of it

**Atum:**
Fixed in [5fa085a](https://github.com/Atum-Labs/solana-escrow/commit/5fa085a4455ebc7ad3cf9d19be5d82608eb0a70a).

**Cyfrin:** Verified.

\clearpage
