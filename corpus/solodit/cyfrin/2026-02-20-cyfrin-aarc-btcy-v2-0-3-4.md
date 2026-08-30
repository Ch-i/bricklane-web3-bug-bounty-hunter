---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Remove redundant modifier from `BTCY, IBTCY::revokeRole`
vuln_class: []
---

# Remove redundant modifier from `BTCY, IBTCY::revokeRole`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `AccessControlUpgradeable::revokeRole` already [has](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/access/AccessControlUpgradeable.sol#L156) modifier `onlyRole(getRoleAdmin(role))` so there is no need to duplicate it in `BTCY::revokeRole`:
```diff
    function revokeRole(bytes32 role, address account)
        public
        override(AccessControlUpgradeable, IAccessControl)
-       onlyRole(getRoleAdmin(role))
    {
        if (role == DEFAULT_ADMIN_ROLE) {
            require(getRoleMemberCount(DEFAULT_ADMIN_ROLE) > 1, CannotRevokeLastAdmin());
        }
        super.revokeRole(role, account);
    }
```

Also affects `IBTCY::revokeRole`.

**Aarc:** Fixed in commit [79b822f](https://github.com/aarc-xyz/btcy-contracts-main/commit/79b822f1c80dcedefac0068e5690e87427772c31).

**Cyfrin:** Verified.
