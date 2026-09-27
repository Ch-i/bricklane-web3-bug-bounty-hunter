---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-unlocker-v2-follow-up-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-unlocker-v2-follow-up
title: '[L-01] Rent is refunded to the wrong address when the pending_amount_claimable_for_cancelled_actuals
  account is closed'
vuln_class: []
---

# [L-01] Rent is refunded to the wrong address when the pending_amount_claimable_for_cancelled_actuals account is closed

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md)_

---

**Files:** [claim_cancelled_actual_tokens.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/unlocker-v2-solana/src/instructions/claim_cancelled_actual_tokens.rs#L154)

**Description:**

The `pending_amount_claimable_for_cancelled_actuals` account is created in the `cancel` instruction, with rent paid by `unlocker.owner`, and is closed in the `claim_cancelled_actual_tokens` instruction, with rent mistakenly refunded to the `receipt` address.

```rust
#[derive(Accounts)]
#[instruction(_project_id: String, _preset_id: u64, _actual_id: u64)]
pub struct ClaimCancelledActualTokens<'info> {
    //...
    #[account(
        mut,
        seeds = [
            b"pending_claimable".as_ref(),
            unlocker.key().as_ref(),
            _preset_id.to_le_bytes().as_ref(),
            _actual_id.to_le_bytes().as_ref(),
        ],
        bump,
        close = recipient // NOTE: We are closing the account here.
    )]
    pub pending_amount_claimable_for_cancelled_actuals: Box<
        Account<'info, PendingAmountClaimableForCancelledActualsAccount>
    >,
    //...
}
```

**Impact:** The `recipient` address will receive the additional rent that should have been refunded to `unlocker.owner`.

**Recommendation:** When closing the `pending_amount_claimable_for_cancelled_actuals` account, the rent should be refunded to `unlocker.owner`.

**Status:** Fixed

**Update from TokenTable:** Funds are now returned to `unlocker.owner` in [a71216f80e80fe9c1e6c62ce8d786d3522a572f7](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/a71216f80e80fe9c1e6c62ce8d786d3522a572f7).
