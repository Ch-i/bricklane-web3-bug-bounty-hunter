---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-atum-solana-v2-0-3-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-atum-solana-v2-0
title: There is not check for the account weather it is the ATA account or not when
  revoking for the delegate account
vuln_class: []
---

# There is not check for the account weather it is the ATA account or not when revoking for the delegate account

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-atum-solana-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md)_

---

**Description:** In order for the authority to revoke the approval of tokens (delegate), he call `Escrow::revoke_delegate`.

When checking for the `authority_ata`, which is the token account that made an approval for `escrow_delegate` to spend on behalf of it. we are only checking the authority of the account without checking the `delegate` address, nor enforcing it is the ATA account.

[escrow::delegate.rs#L51-L56](https://github.com/Atum-Labs/solana-escrow/blob/main/programs/escrow/src/instructions/delegate.rs#L51-L56)
```rust
pub struct RevokeDelegate<'info> {
    ...
    /// The authority's token account where delegation was approved
    #[account(
        mut,
        constraint = authority_ata.owner == authority.key() @ ErrorCode::InvalidAuthority,
        constraint = authority_ata.mint == escrow_delegate.allowed_mint @ ErrorCode::InvalidMint,
    )]
    ...
}
```

So when calling revoke on the token account we can endup of revoking from another account (ruther than the ATA account) owned by that authority instead of the actual owner ATA account that made approval to `escrow_delegate`.

**Impact:**
- closing `escrow_delegate` account without revoking delegation

**Proof of Concept:**
- Bob has accounts for the same Mint (one is the ATA, and another one)
- He used one of them and called `escrow::create_delegate()`
- He wants to revoke this
- He calls `escrow::revoke_delegate()` but he put the other account instead of the ATA as ` authority_ata`
- Checks for `authority_ata` gets passed, same owner, same mint
- Revoking occur for the second account that was not used at `escrow::create_delegate()`
- `escrow_deposit` account gets closed
- The original ATA still has delegate

**Recommended Mitigation:** We should check that `delegate` made to `escrow_delegate`, or to be more accurate we should make sure the account passed is the ATA account.

**Atum:**
Fixed in [0800928](https://github.com/Atum-Labs/solana-escrow/commit/0800928dd7695c4e4cf7539df2a5f533c77e3817).

**Cyfrin:** Verified.
