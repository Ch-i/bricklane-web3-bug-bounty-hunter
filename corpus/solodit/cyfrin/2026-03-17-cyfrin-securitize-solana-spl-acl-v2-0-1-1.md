---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: '`thaw_permissionless` and `freeze_permissionless` Can Be Bypassed by Direct
  `token_acl` Invocation'
vuln_class: []
---

# `thaw_permissionless` and `freeze_permissionless` Can Be Bypassed by Direct `token_acl` Invocation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** The `is_paused` check in `thaw_permissionless_handler` and `freeze_permissionless_handler` only applies when users invoke the spl-token-access-control program. Users can bypass this check by calling the `token_acl` program directly, since `token_acl` does not enforce the ACL program's pause state. The admin's ability to pause permissionless thaw/freeze operations is therefore ineffective for direct `token_acl` callers.

The ACL program checks `AccessControlState.is_paused` before CPI-ing to token_acl:

```rust
    require!(
        !ctx.accounts.access_control_state.is_paused,
        AccessControlError::Paused
    );
```
The same check exists in `freeze_permissionless_handler`.

However, the `token_acl` program  is a separate, publicly callable program. Users can construct transactions that invoke token_acl's `thaw_permissionless` (or `freeze_permissionless`) instruction directly, without going through `spl-token-access-control`. The `token_acl` program does not read or validate `AccessControlState` as it only invokes the gating program for its own checks.


**Impact:** When the admin pauses the ACL program, they may expect all permissionless thaw/freeze operations to stop. In reality, users who call `token_acl` directly can still thaw or freeze accounts.

**Recommended Mitigation:** If the team intends pause to apply to all permissionless thaw/freeze operations, the check must be enforced in a place that cannot be bypassed. The `token_acl` program invokes the gating program for its gating logic. The gating program is the single point through which all thaw/freeze permissionless flows pass.

**Securitize:** Fixed in [d041c66](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/d041c6692a66bac24a12d12c31acf2c020797684).

**Cyfrin:** Verified.

\clearpage
