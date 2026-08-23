---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-0
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
title: '`calculate_jump_price` requires mint decimals <= 18 but initialize and `update_jump_pool_config`
  never validate the bound'
vuln_class: []
---

# `calculate_jump_price` requires mint decimals <= 18 but initialize and `update_jump_pool_config` never validate the bound

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** `calculate_jump_price` opens with `require!(asset_decimals <= WAD_SCALE && liquidity_decimals <= WAD_SCALE, JumpRouterError::InvalidDecimals)` (`programs/bc-solana-jump-router-sc/src/utils/swap_utils.rs:26-35`). This check runs on every swap before collar and event-price calculations. Because Solana mint decimals are a `u8` field, any configured mint with more than 18 decimals will make every swap revert with `InvalidDecimals`.

The mints are registered through the `Initialize` accounts and `initialize_handler` (`programs/bc-solana-jump-router-sc/src/instructions/admin/initialize.rs:49-69, 120-127`) and can be replaced through `update_jump_pool_config_handler` (`programs/bc-solana-jump-router-sc/src/instructions/admin/update_jump_pool_config.rs:27-47, 88-99`). Neither path checks `asset_mint.decimals` or `liquidity_mint.decimals` before storing the config.

**Impact:** If an asset or liquidity mint with decimals greater than 18 is registered, all swap instructions for that router instance will revert when price calculation runs. No trade can settle and no fees are collected until the config is corrected. If correction is not possible operationally, recovery requires creating or routing through another router instance.

**Recommended Mitigation:** Add decimals-bound checks in both `initialize_handler` and `update_jump_pool_config_handler`, requiring `asset_mint.decimals <= WAD_SCALE` and `liquidity_mint.decimals <= WAD_SCALE` before storing the pool config.

**Securitize:** Fixed in [297935b](https://github.com/securitize-io/bc-bd-router-sc/commit/297935b170108eda435c0f829c6dd160625d620b).

**Cyfrin:** Verified.
