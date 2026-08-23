---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: '`MbpsFeeManager::validate` performs no external fee collector zero-address
  rejection required by the design specification'
vuln_class: []
---

# `MbpsFeeManager::validate` performs no external fee collector zero-address rejection required by the design specification

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The design specification requires the program to reject a zero external fee collector when an external fee is non-zero. The current external-fee validation checks the caller-supplied external manager and associated token account, but it does not reject `Pubkey::default()`.

`SwapAccounts::validate_external_fee_config` validates that:

- the external manager passes `external_fee_manager.validate()`;
- `external_fee_manager.fee_collector_wallet()` equals the supplied `external_fee_collector_wallet`;
- `external_fee_collector_ata` is the expected ATA for that wallet, the liquidity mint, and the liquidity token program;
- the ATA mint, owner, and account owner match the expected values.

Those checks are at `programs/bc-solana-jump-router-sc/src/instructions/swap_accounts.rs:171-212`.

`MbpsFeeManager::validate` only enforces the fee numerator cap (`programs/bc-solana-jump-router-sc/src/states/fee_manager/mpbs_fee_manager.rs:42-48`). It does not inspect `collector_wallet`. Therefore an external manager with a non-zero numerator and `collector_wallet = Pubkey::default()` is not rejected by the fee-manager validation itself. If the caller supplies the corresponding zero-authority ATA, the external fee can be routed to an address with no recoverable private signer.

This is no longer the same issue as the earlier stale `active_fee_manager` wording: the protocol fee collector is still validated against `jump_router_state.fee_manager.fee_collector_wallet()` at `swap_accounts.rs:111-115`, and protocol fees are still transferred to `fee_collector_ata`. The missing guard is specific to the additional external fee recipient.

**Impact:** When an external fee manager with a non-zero numerator uses the default public key as the collector, the external fee may be transferred to an unrecoverable zero-authority ATA instead of a valid integrator collector. The stored Securitize protocol fee is unaffected because it is collected through the configured protocol fee collector.

**Recommended Mitigation:** Reject `Pubkey::default()` in the external-fee validation path before any fund movement. At minimum, enforce this when `external_fee_manager` has a non-zero numerator. A stricter and simpler approach is to reject a default external collector whenever `external_fee_manager.is_some()`.

**Securitize:** Fixed in [64086a4](https://github.com/securitize-io/bc-bd-router-sc/commit/64086a4504406d4bf74ee24bbc8c9eae8ca36fb4).

**Cyfrin:** Verified.
