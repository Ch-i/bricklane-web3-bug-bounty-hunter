---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-1-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: '`tracker_account` binding is not validated upfront in `bridge_ds_tokens`'
vuln_class: []
---

# `tracker_account` binding is not validated upfront in `bridge_ds_tokens`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** In `bridge_ds_tokens`, `tracker_account` is accepted as an unchecked, caller-supplied account and is read by the bridge's own lock-up gate (`validate_locked_tokens`) before any binding to the current `(asset_mint, identity_account)` pair is verified. The only effective binding enforcement happens several CPIs later inside the Policy Engine (`update_counters_on_burn`). For defense in depth, the bridge should validate `tracker_account` at the front, before relying on its contents.


`tracker_account` is declared as an `UncheckedAccount` with no PDA seeds and no relationship to `identity_account` or `asset_mint`:

```159:161:bc-solana-bridge-sc/programs/securitize_bridge/src/instructions/bridge/bridge_ds_tokens.rs
    /// CHECK: Passed to RBAC CPI and validate_locked_tokens.
    #[account(mut)]
    pub tracker_account: UncheckedAccount<'info>,
```


**Impact:** If a mismatched `tracker_account` is supplied, the Policy Engine CPI eventually reverts. However, correctness currently depends on an unrelated downstream program several CPIs away.

**Recommended Mitigation:** The project should address this in one of two ways:
- either fix it in code
- or make the deferred-validation design explicit in documentation.

**Securitize:** Fixed in commit [318bdd5](https://github.com/securitize-io/bc-solana-bridge-sc/commit/318bdd51a3e5f1ca16c31059402d8bbdc5ba0f21). validate_locked_tokens now validates the tracker_account binding upfront, before relying on its contents: it asserts tracker.asset_mint equals the bridge's asset_mint and tracker.identity_account equals the supplied identity_account, returning a new TrackerAccountMismatch error on mismatch. The bridge no longer depends on the downstream Policy Engine CPI to catch a mismatched tracker — the binding is enforced at the front of bridge_ds_tokens.

**Cyfrin:** Verified.
