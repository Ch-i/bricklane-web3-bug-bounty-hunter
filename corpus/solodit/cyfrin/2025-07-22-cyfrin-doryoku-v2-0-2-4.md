---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Unnecessary Utility Functions in the `xbelo` Program
vuln_class: []
---

# Unnecessary Utility Functions in the `xbelo` Program

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** `xgkhan` program has some functions that are neither utilized nor necessary:
- `transfer_hook()`: `xGKHAN` is a regular SPL token, not a TOKEN2022 token with extensions. Hence there is no need for a hook function.
- `transfer_xgkhan()`: This custom transfer function, which always fails, does not provide any functionality. Since `xGKHAN` tokens became frozen after they are minted to user, transfers will fail at the token program level. This function won't be utilized during token transfers.
- `verify_non_transferable()`: SPL token accounts already have built-in freeze status checking functionality via `TokenAccount::is_frozen` function. Both of these functions checks the same state, hence it is not necessary to provide a functionality that is already available in the token program itself.

**Recommended Mitigation:** Consider removing aforementioned functions and their instruction context (Accounts struct).

**Doryoku:**
Fixed in [41676f1](https://github.com/Warlands-Nft/xbelo/commit/41676f1ad0572f9b08fcd53c1d0a4a39b4fb9685).

**Cyfrin:** Verified.
