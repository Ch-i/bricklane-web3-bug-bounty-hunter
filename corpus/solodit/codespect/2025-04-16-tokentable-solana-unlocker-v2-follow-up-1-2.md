---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-unlocker-v2-follow-up-1-2
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
title: '[L-03] The creation of pending_amount_claimable_for_cancelled_actuals account
  may lead to rent loss'
vuln_class: []
---

# [L-03] The creation of pending_amount_claimable_for_cancelled_actuals account may lead to rent loss

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md)_

---

**Files:** [cancel.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/unlocker-v2-solana/src/instructions/cancel.rs#L72)

**Description:**

The `pending_amount_claimable_for_cancelled_actuals` account is always created with rent paid by `unlocker.owner`. However, when `should_wipe_claimable_balance` is true or `delta_amount_claimable` is 0, the account cannot be closed in the `claim_cancelled_actual_tokens` instruction.

```rust
fn _claim_pending_amount(
    ctx: Context<ClaimCancelledActualTokens>,
    project_id: String,
    actual_id: u64,
    batch_id: u64
) -> Result<()> {
    let delta_amount_claimable =
        ctx.accounts.pending_amount_claimable_for_cancelled_actuals.pending_amount_claimable_for_cancelled_actuals;
    require!(delta_amount_claimable != 0, TokenTableError::NotClaimable);
    // ...
}
```

**Impact:** The `pending_amount_claimable_for_cancelled_actuals` account cannot be closed, causing the rent to be locked.

**Recommendation:** It is recommended not to create the `pending_amount_claimable_for_cancelled_actuals` account when `should_wipe_claimable_balance` is true and to directly close the account when `delta_amount_claimable` is 0.

**Status:** Fixed

**Update from TokenTable:** In [9f97ad413026962fd0d544be537d634aebba401c](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/9f97ad413026962fd0d544be537d634aebba401c), automatically close `pending_amount_claimable_for_cancelled_actuals` account in `cancel()` if `should_wipe_claimable_balance` is true or `delta_amount_claimable` is 0. Also, allow `claim_cancelled_actual_tokens()` to close the `pending_amount_claimable_for_cancelled_actuals` account if `delta_amount_claimable` is 0 and the account already exists.
