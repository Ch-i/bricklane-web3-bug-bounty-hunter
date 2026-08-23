---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: '`RedemptionCompleted` emits gross liquidity output rather than the user''s
  net received amount'
vuln_class: []
---

# `RedemptionCompleted` emits gross liquidity output rather than the user's net received amount

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The `RedemptionCompleted` event currently reports the gross `received_liquidity_amount` instead of the net `liquidity_amount_net` actually transferred to the user after fees. This does not affect fund safety, but it weakens event accuracy and can mislead off-chain accounting, analytics, and monitoring systems.


In the `AssetForLiquidity` flow, the program first computes the gross amount returned by the pool, then derives the net user amount by subtracting protocol and optional external fees:

```rust
let liquidity_fee_amount = jump_router_state
    .fee_manager
    .calculate_fee(quoted_liquidity_amount)?;

let liquidity_external_fee_amount = match external_fee_manager {
    Some(manager) => manager.calculate_fee(quoted_liquidity_amount)?,
    None => 0,
};

let liquidity_amount_net = quoted_liquidity_amount
    .checked_sub(liquidity_fee_amount)
    .and_then(|x| x.checked_sub(liquidity_external_fee_amount))
    .ok_or(JumpRouterError::MathOverflow)?;
```

The user then receives `liquidity_amount_net`:

```rust
crate::transfer_tokens!(
    &swap_accounts.liquidity_router_vault,
    &swap_accounts.liquidity_user_ata,
    &swap_accounts.jump_router_authority,
    &swap_accounts.liquidity_program,
    &swap_accounts.liquidity_mint,
    liquidity_amount_net,
    swap_accounts.liquidity_mint.decimals,
    router_authority_signer
);
```

However, the emitted event reports the gross amount instead:

```rust
emit_cpi!(crate::events::RedemptionCompleted {
    off_ramp: jump_router_state.key(),
    redeemer: swap_accounts.user.key(),
    asset_amount: amount_in,
    liquidity_amount: received_liquidity_amount,
    fee_amount: liquidity_fee_amount,
    rate: denormalized_jump_price,
});
```

As a result, consumers relying only on the event may infer that the user received more liquidity than was actually credited to their account.

**Impact:** This issue is limited to observability and reporting quality. It can cause discrepancies in indexers, reconciliation pipelines, dashboards, or downstream integrations that assume the event reflects the user's net settlement amount.

**Recommended Mitigation:** Consider emitting the net amount delivered to the user, or extend the event to include both gross and net values explicitly. This preserves full transparency while allowing off-chain consumers to reason about settlement and fees without reconstructing them manually.


**Securitize:** Fixed in [bc33a93](https://github.com/securitize-io/bc-bd-router-sc/commit/bc33a936c4241b244f9c24c721c53d81c8fa23d0).

**Cyfrin:** Verified.
