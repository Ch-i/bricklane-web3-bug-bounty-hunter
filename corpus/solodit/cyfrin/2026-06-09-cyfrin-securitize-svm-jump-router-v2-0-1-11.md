---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-11
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
title: Fee collector default pubkey Is not rejected while Initialization
vuln_class: []
---

# Fee collector default pubkey Is not rejected while Initialization

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** During router initialization, the program validates that `fee_collector_wallet` matches the wallet configured in `fee_manager`, but it does not explicitly reject `Pubkey::default()`.

However, `UpdateFeeManager` applies a stricter check and correctly rejects the default pubkey:
```rust
fee_collector_wallet.key() == fee_manager.fee_collector_wallet()
    && fee_collector_wallet.key() != Pubkey::default()
```
This creates inconsistent validation between initialization and later fee-manager updates. If a router is initialized with the default pubkey as the fee collector wallet, protocol fees may be transferred to the associated token account owned by the default pubkey.

This is mainly a defense-in-depth/configuration issue because initialization is permissioned, but it can still cause permanent loss of fee revenue if misconfigured.

**Recommended Mitigation:** Apply the same non-default wallet validation during initialization as well:
```rust
#[account(
    constraint = fee_collector_wallet.key() == fee_manager.fee_collector_wallet()
        && fee_collector_wallet.key() != Pubkey::default()
            @ JumpRouterError::InvalidFeeCollector,
)]
pub fee_collector_wallet: UncheckedAccount<'info>,
```
Also consider enforcing this inside `FeeManager::validate()` so all fee-manager entry points share the same invariant.

**Securitize:** Fixed in [64086a4](https://github.com/securitize-io/bc-bd-router-sc/commit/64086a4504406d4bf74ee24bbc8c9eae8ca36fb4).

**Cyfrin:** Verified.
