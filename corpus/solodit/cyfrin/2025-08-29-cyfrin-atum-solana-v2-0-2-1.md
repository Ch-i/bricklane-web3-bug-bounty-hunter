---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-atum-solana-v2-0-2-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-atum-solana-v2-0
title: Creating delegation with different `delegate_signer` will override prev one
vuln_class: []
---

# Creating delegation with different `delegate_signer` will override prev one

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-atum-solana-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md)_

---

**Description:** When creating delegation escrow account is created passed on `authority` and `delegate_signer`. where delegate signer is authorized for making deposits on behave of the owner.

[delegate.rs#L15-L22](https://github.com/Atum-Labs/solana-escrow/blob/main/programs/escrow/src/instructions/delegate.rs#L15-L22)
```rust
pub struct CreateDelegate<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    #[account(
        init,
        payer = payer,
        space = EscrowDelegate::LEN,
>>      seeds = [b"escrow_delegate", authority.key().as_ref(), delegate_signer.as_ref()],
        bump
    )]
    pub escrow_delegate: Account<'info, EscrowDelegate>,
    #[account(
        init_if_needed,
        payer = payer,
        associated_token::mint = mint,
        associated_token::authority = authority,
        associated_token::token_program = token_program,
    )]
    pub authority_ata: InterfaceAccount<'info, TokenAccount>,
    ...
}
```

The authority account is restricted to be ATA account, since each Account can have only one ATA, so if they delegated to another `delegate_signer` the delegation will be created successfully, making another `escrow_delegate`, but the actual ATA for the authority will override `delegate_signer_1` to `delegate_signer_2` and `remaining_capacity_1` to `remaining_capacity_2` leaving the old escrow_delegate as it is.

**Impact:**
- Creating another delegation will revoke the previous one without closing the old `escrow_delegate`
- Users are prevented from making more than one delegation for the same mint

**Recommended Mitigation:** We should remove `delegate_signer` from the seed when creating/deriving `escrow_delegate` account, as since we are depending on ATA account, users will have only one delegate

**Atum:**
Fixed in [f53dff6](https://github.com/Atum-Labs/solana-escrow/commit/f53dff66146c9df3f1b1161e3aea69e360635725).

**Cyfrin:** Verified.


\clearpage
