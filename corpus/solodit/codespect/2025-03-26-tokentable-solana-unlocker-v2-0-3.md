---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-0-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[M-04] The pending_amount_claimable accumulated in the cancel instruction
  cannot be claimed'
vuln_class: []
---

# [M-04] The pending_amount_claimable accumulated in the cancel instruction cannot be claimed

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`cancel.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/cancel.rs#L37)

**Description:**

In the `cancel()` instruction, if `should_wipe_claimable_balance` is false, the unclaimed rewards of the closed `ActualAccount` will be accumulated into the `PendingAmountClaimableForCancelledActualsAccount` account.

```rust
fn _cancel(
  ctx: Context<Cancel>,
  actual_id: u64,
  should_wipe_claimable_balance: bool,
  batch_id: u64
) -> Result<()> {
  let delta_amount_claimable = _calculate_amount_claimable(
    ctx.accounts.actual.clone(),
    ctx.accounts.preset.clone()
  )?.delta_amount_claimable;

  if !should_wipe_claimable_balance {
    ctx.accounts.pending_amount_claimable_for_cancelled_actuals.pending_amount_claimable_for_cancelled_actuals +=
      delta_amount_claimable;
  }
  //...
}
```

However, the user is unable to claim the accumulated balance in the `PendingAmountClaimableForCancelledActualsAccount` because the balance can only be claimed through the `claim()` and `delegate_claim()` instructions, both of which require the `ActualAccount` that has been closed by the `cancel()` instruction. Additionally, the corresponding `ActualAccount` cannot be re-init.

**Impact:** The user may lose the unclaimed tokens from before the execution of the cancel instruction.

**Recommendation:** It is recommended to separate the logic for claiming the tokens accumulated in `PendingAmountClaimableForCancelledActualsAccount` from the `claim()` and `delegate_claim()` instructions.

**Status:** Fixed

**Update from TokenTable:** Restructured the claiming process in [f851e215e19904ea9a1d07cfa44b9cc34afce11e](https://github.com/EthSign/tokentable-unlocker-solana/tree/f851e215e19904ea9a1d07cfa44b9cc34afce11e). `delegate_claim()` has been combined into `claim()` with logic changes pertaining to authority, recipient, and `recipient_ata` accounts. Split `claim()` logic into `claim()` and `claim_cancelled_actual_tokens()` in order to allow claiming the previously orphaned tokens present in `PendingAmountClaimableForCancelledActualsAccount`.
