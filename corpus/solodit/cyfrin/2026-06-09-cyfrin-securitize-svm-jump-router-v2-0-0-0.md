---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: '`ExecuteSwap::swap_asset_for_liquidity` charges the sell-path fee on JUMP
  output instead of the QUODD-referenced input'
vuln_class: []
---

# `ExecuteSwap::swap_asset_for_liquidity` charges the sell-path fee on JUMP output instead of the QUODD-referenced input

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The sell path computes both liquidity-denominated fees from JUMP's realized output rather than from the QUODD/NBBO-referenced input value.

In the current shared swap implementation, `swap_asset_for_liquidity` obtains the JUMP quote and then calculates the protocol fee from `quoted_liquidity_amount`:

```rust
let liquidity_fee_amount = jump_router_state
    .fee_manager
    .calculate_fee(quoted_liquidity_amount)?;
```

It applies the same output-based fee base to any external fee manager:

```rust
let liquidity_external_fee_amount = match external_fee_manager {
    Some(manager) => manager.calculate_fee(quoted_liquidity_amount)?,
    None => 0,
};
```

These lines are in `programs/bc-solana-jump-router-sc/src/instructions/swap_accounts.rs:466-490`.

`quoted_liquidity_amount` is JUMP's actual USDC quote, not the QUODD/NBBO reference value. On the standard operator-gated path, `nbbo_price` is supplied by `execute_swap_handler` and passed into `SwapAccounts::execute_swap` (`programs/bc-solana-jump-router-sc/src/instructions/operator/execute_swap.rs:20-55`). On the headless path, no NBBO value is available; `execute_swap_headless_handler` intentionally passes `None` for `nbbo_price` (`programs/bc-solana-jump-router-sc/src/instructions/user/execute_swap_headless.rs:29-37`).

The protocol specification describes the sell-side Securitize fee as a fixed fee on the input token's USDC-equivalent value at the QUODD/NBBO reference. Under the current implementation, if JUMP delivers more liquidity than the NBBO-equivalent amount, the protocol fee and external fee are also charged on the positive execution improvement. The buy path is different: it computes fees from `amount_in` before sending the post-fee amount to JUMP (`swap_accounts.rs:270-278`).

**Impact:** For standard operator-gated sell swaps where JUMP's execution beats the QUODD/NBBO reference, users pay fee_bps on the positive execution improvement instead of receiving that improvement in full. The overcharge is bounded by the configured positive-slippage collar on the standard path. The current headless path has no NBBO input, so the NBBO-referenced sell-fee model cannot be implemented for headless swaps without changing either the API or the documented headless behavior.

**Recommended Mitigation:** For standard `execute_swap`, compute the sell-path protocol fee from the NBBO-equivalent liquidity value rather than `quoted_liquidity_amount`. If the external fee is intended to follow the same basis, compute it from the same reference amount. If the current output-based model is intended, update the specification to state that sell fees are charged on realized JUMP output.

For `execute_swap_headless`, either document that sell fees are output-based because no NBBO is supplied, or add a headless NBBO/reference input if headless swaps must also use the QUODD-referenced fee model.

**Securitize:** Acknowledged; I believe this is a doc error, and we intentionally deduct fee from the real swap amount.
