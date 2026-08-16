---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: Whitelist pause does not stop investor registry create/delete paths
vuln_class: []
---

# Whitelist pause does not stop investor registry create/delete paths

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** The main `whitelist` instruction checks the global pause flag:
```rust
require!(
    !ctx.accounts.spl_whitelist_state.is_paused,
    SplWhitelistErrorCode::Paused
);
```
However, the direct registry mutation paths do not check `is_paused`. So, while paused, the combined whitelist/thaw flow is blocked, but authorized callers can still create or delete InvestorRegistry records directly.

**Impact:** If pause is intended as an emergency stop for all whitelist-related state changes, this creates a bypass. During a pause, admin or freeze-authority accounts can still alter which wallets are considered registered for SPL bridge usage.

**Recommended Mitigation:** Add the same pause guard to create_investor_registry_handler and delete_investor_registry_handler.

**Securitize:** Acknowledged — keeping as-is by design. create_investor_registry and delete_investor_registry are privileged admin/freeze-authority instructions, not permissionless user paths.

**Cyfrin:** The team acknowledged as by design since these are privileged instructions.

\clearpage
