---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-02-cyfrin-atum-solana-v2-v2-0-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-04-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-02-cyfrin-atum-solana-v2-v2-0
title: Missing mint validation in `CreateDelegate`
vuln_class: []
---

# Missing mint validation in `CreateDelegate`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-02-cyfrin-atum-solana-v2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md)_

---

**Description:** The CreateDelegate instruction creates an `EscrowDelegate` account and approves token delegation without verifying that the mint is on the protocol's allowlist (i.e., that a `MintFeeConfig` PDA exists for the mint).

In contrast, the `deposit` function in `escrow.rs` does validate the mint allowlist:
```rust
// In deposit handler:
let mint_fee_config_info = &ctx.accounts.mint_fee_config;
require!(
    !mint_fee_config_info.data_is_empty(),
    ErrorCode::MintNotAllowed
);
```
This means users can create delegate accounts for mints that are not allowed by the protocol. When they later attempt to deposit using this delegate, the transaction will fail with `MintNotAllowed`, but the rent paid for the `EscrowDelegate` account (128 bytes) has already been spent.

**Impact:** Users pay rent to create accounts that are immediately unusable if the mint is not allowlisted.

**Recommended Mitigation:** Add a `MintFeeConfig` account check to the `CreateDelegate` instruction to ensure the mint is on the allowlist before creating the delegate

**Atum:** Fixed in [b4c128e](https://github.com/Atum-Labs/solana-escrow/commit/b4c128e78d8b91112a242b652cfb8b8f4ee0e736).

**Cyfrin:** Verified.
