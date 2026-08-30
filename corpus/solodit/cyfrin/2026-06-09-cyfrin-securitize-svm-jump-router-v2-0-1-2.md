---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-2
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
title: '`UpdateJumpPoolConfig::update_jump_pool_config` repoints mints but does not
  reset `min_asset_amount_in, min_liquidity_amount_in`'
vuln_class: []
---

# `UpdateJumpPoolConfig::update_jump_pool_config` repoints mints but does not reset `min_asset_amount_in, min_liquidity_amount_in`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** `update_jump_pool_config_handler` replaces `jump_router_state.jump_pool_config` with the new config, which may carry different `asset_mint` and `liquidity_mint` values with different decimal scales (`programs/bc-solana-jump-router-sc/src/instructions/admin/update_jump_pool_config.rs:88-99`). The mint accounts used by the update are checked only for key and token-program consistency (`update_jump_pool_config.rs:27-47`).

`min_asset_amount_in` and `min_liquidity_amount_in` are stored in `JumpRouterState` as native token-unit thresholds denominated in the respective mint's decimals. The handler does not reset or rescale those fields after changing the pool config.

If the new mints have a different decimal scale from the previous mints, the stored thresholds become mis-denominated. For example, if `min_asset_amount_in` was set to `1_000_000` for a 6-decimal asset mint and the config is updated to a 9-decimal asset mint, the threshold now represents `0.001` tokens rather than `1` token. The reverse migration can make the threshold unexpectedly large and block swaps until corrected.

**Impact:** After a pool config update that changes mint decimals, the minimum trade thresholds silently apply the wrong effective minimum. The issue is admin-recoverable by calling the threshold setters, but there is a misconfiguration window between the pool update and the corrective threshold updates.

**Recommended Mitigation:** Reset `min_asset_amount_in` and `min_liquidity_amount_in` when the configured mints change, or require the new thresholds to be supplied in the same instruction/transaction. If the current behavior is intended, document the required operational sequence: update pool config, then immediately update both minimum thresholds for the new mint units.

**Securitize:** Fixed in [90b345b](https://github.com/securitize-io/bc-bd-router-sc/commit/90b345b1ca4b89cac2194b1c39a7784053d30141).

**Cyfrin:** Verified.
