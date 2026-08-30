---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: '`JumpRouterState` collar and min-amount parameters have no bounds at init
  or in their setters'
vuln_class: []
---

# `JumpRouterState` collar and min-amount parameters have no bounds at init or in their setters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** Three `JumpRouterState` parameters are written without range validation.

First, `initialize_handler` stores `max_positive_slippage_mbps` verbatim (`programs/bc-solana-jump-router-sc/src/instructions/admin/initialize.rs:120-145`), and `update_max_positive_slippage_handler` only checks that the new value differs from the current one (`programs/bc-solana-jump-router-sc/src/instructions/admin/update_max_positive_slippage.rs:20-32`). No minimum or maximum is enforced.

The positive-slippage collar only applies when `nbbo_price_opt` is `Some`. That means it applies to standard operator-gated swaps, where `operator/execute_swap.rs` passes `Some(nbbo_price)` (`programs/bc-solana-jump-router-sc/src/instructions/operator/execute_swap.rs:47-55`), but not to headless swaps, where `execute_swap_headless_handler` passes `None` (`programs/bc-solana-jump-router-sc/src/instructions/user/execute_swap_headless.rs:29-37`). When the collar is active, the buy and sell checks use the stored value at `swap_accounts.rs:315-323` and `swap_accounts.rs:505-513`.

Second, `min_asset_amount_in` and `min_liquidity_amount_in` are updated by setters that only check `new != old` (`programs/bc-solana-jump-router-sc/src/instructions/admin/update_min_asset_amount_in.rs:20-32`, `programs/bc-solana-jump-router-sc/src/instructions/admin/update_min_liquidity_amount_in.rs:20-32`). These thresholds apply to both standard and headless swaps at `swap_accounts.rs:263-265` and `swap_accounts.rs:448-450`.

**Impact:** An admin can accidentally set `max_positive_slippage_mbps` so low that standard favorable-price swaps revert, or so high that the standard path's positive-slippage collar is effectively disabled. Separately, an admin can set either minimum input threshold above realistic trade sizes, DoSing the affected direction for both standard and headless swaps until corrected. Recovery is possible through admin updates, so the impact is operational rather than permanent.

**Recommended Mitigation:** Define and enforce acceptable bounds for `max_positive_slippage_mbps`, `min_asset_amount_in`, and `min_liquidity_amount_in` at initialization and in their setters. If exact bounds are business-configurable, document them and add defensive upper limits that prevent accidental all-swap DoS.

**Securitize:** Acknowledged; We don't need those limits, we understand the risk of an operator setting wrong values, but at the same time we can fix it easily. In the headless flow NBBO is not used at all, so the max positive slippage value will not be used because there is no reference price to compare against.
