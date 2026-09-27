---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[L-03] Missing check whether fee_token and token_mint are consistent in the
  init_fee_token instruction'
vuln_class: []
---

# [L-03] Missing check whether fee_token and token_mint are consistent in the init_fee_token instruction

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`init_fee_token.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/fee-collector/src/instructions/init_fee_token.rs)

**Description:**

In the `init_fee_token` instruction, there is no check to ensure that `fee_token` and `token_mint` are consistent. This may result in the vault account’s seed not matching the corresponding mint. Causing the vault account to be unable to properly collect fees.

```rust
pub struct InitFeeToken<'info> {
  //...
  #[account(
    init_if_needed,
    payer = authority,
    seeds = [b"vault".as_ref(), fee_token.as_ref()],
    bump,
    token::mint = token_mint,
    token::authority = storage
  )]
  pub vault: Option<InterfaceAccount<'info, TokenAccount>>,
  pub token_mint: Option<InterfaceAccount<'info, Mint>>,
  //...
}
```

**Impact:** When `fee_token` and `token_mint` are inconsistent, the vault account created by the `init_fee_token` instruction will be unable to properly receive fees.

**Recommendation:** It is recommended to check that `fee_token` and `token_mint` are the same.

**Status:** Fixed

**Update from TokenTable:** Added constraint to `token_mint` in [eb09b6b3d1da4774d72cd75b99e7eb9cf86bb7e9](https://github.com/EthSign/tokentable-unlocker-solana/tree/eb09b6b3d1da4774d72cd75b99e7eb9cf86bb7e9).
