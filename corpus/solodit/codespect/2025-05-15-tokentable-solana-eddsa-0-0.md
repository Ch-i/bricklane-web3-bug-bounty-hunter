---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-05-15-tokentable-solana-eddsa-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-05-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-05-15-TokenTable-Solana-EDDSA.md
tags:
- firm:codespect
- report:2025-05-15-tokentable-solana-eddsa
title: '[H-01] Missing fee_collector check in the Claim instruction'
vuln_class: []
---

# [H-01] Missing fee_collector check in the Claim instruction

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-05-15-TokenTable-Solana-EDDSA.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-05-15-TokenTable-Solana-EDDSA.md)_

---

**Files:** [claim.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/87b79fe77b74d734fc5274da93300aa39444146c/programs/eddsa-token-distributor-solana/src/instructions/claim.rs#L123), [claim.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/87b79fe77b74d734fc5274da93300aa39444146c/programs/eddsa-token-with-fees-distributor-solana/src/instructions/claim.rs#L115)

**Description:**

In the `Claim` instruction, `fee_collector` is not verified in the ctx, and no check is performed in the subsequent handler function either.

```rust
#[derive(Accounts)]
#[instruction(_project_id: String, _recipient: Pubkey, _claim_id: [u8; 32])]
pub struct Claim<'info> {
    //...
    #[account(mut)]
    pub fee_collector_vault: Option<UncheckedAccount<'info>>,
    /// CHECK: Checked in the function call.
    pub fee_collector: UncheckedAccount<'info>,
    //...
}
```

**Impact:** A malicious actor can pass in a malicious program to bypass fee payment.

**Recommendation(s):** It is recommended to verify that the `fee_collector` passed in the instruction matches the one recorded in the `airdrop` account

**Status:** Fixed

**Update from TokenTable:** Added fee collector account constraint in [f934c5c727a9bf5cf6bc3dbd362b957a9d4f90ea](https://github.com/EthSign/tokentable-unlocker-solana/commit/f934c5c727a9bf5cf6bc3dbd362b957a9d4f90ea).
