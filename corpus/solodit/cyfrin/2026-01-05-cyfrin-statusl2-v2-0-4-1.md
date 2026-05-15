---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Inconsistent naming in `Karma._onlySlasher`
vuln_class: []
---

# Inconsistent naming in `Karma._onlySlasher`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** `_onlySlasher` allows Admin to perform an operation same as `_onlyAdminOrOperator`, however you don't include Admin to naming:
```solidity
    function _onlyAdminOrOperator(address sender) internal view {
        if (!hasRole(DEFAULT_ADMIN_ROLE, sender) && !hasRole(OPERATOR_ROLE, sender)) {
            revert Karma__Unauthorized();
        }
    }

    //@audit INFO. Inconsistent naming с предыдущим
    function _onlySlasher(address sender) internal view {
        if (!hasRole(DEFAULT_ADMIN_ROLE, sender) && !hasRole(SLASHER_ROLE, sender)) {
            revert Karma__Unauthorized();
        }
    }
```

**Recommended Mitigation:**
```diff
-   modifier onlySlasher() {
+   modifier onlyAdminOrSlasher() {
-       _onlySlasher(msg.sender);
+       _onlyAdminOrSlasher(msg.sender);
        _;
    }

-   function _onlySlasher(address sender) internal view {
+   function _onlyAdminOrSlasher(address sender) internal view {
        if (!hasRole(DEFAULT_ADMIN_ROLE, sender) && !hasRole(SLASHER_ROLE, sender)) {
            revert Karma__Unauthorized();
        }
    }


```

**StatusL2:** Fixed in [030efdd](https://github.com/status-im/status-network-monorepo/commit/030efdda72d94969304d2f377ceeb9fc38d5a05a).

**Cyfrin:** Verified.
