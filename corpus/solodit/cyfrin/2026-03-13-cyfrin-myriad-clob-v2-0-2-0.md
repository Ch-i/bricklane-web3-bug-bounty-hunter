---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`AdminRegistry::proposeAdmin` self-proposal permanently removes `DEFAULT_ADMIN_ROLE`'
vuln_class: []
---

# `AdminRegistry::proposeAdmin` self-proposal permanently removes `DEFAULT_ADMIN_ROLE`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `proposeAdmin` has no guard against an admin proposing their own address:

```solidity
// AdminRegistry.sol:33-38
function proposeAdmin(address newAdmin) external {
    require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender), "not admin");
    require(newAdmin != address(0), "zero address");
    pendingAdmin = newAdmin; // no check: newAdmin != admin
    emit AdminProposed(newAdmin);
}
```

When the current admin then calls `acceptAdmin()`:

```solidity
address oldAdmin = admin;                          // == msg.sender
_grantRole(DEFAULT_ADMIN_ROLE, pendingAdmin);      // no-op — already held
_revokeRole(DEFAULT_ADMIN_ROLE, oldAdmin);         // REMOVES the role from the same address
admin = pendingAdmin;                              // no change to state variable
pendingAdmin = address(0);
```

The `_grantRole` is a no-op because the pending admin already holds the role. `_revokeRole` then strips it. After the call the `admin` state variable still points to the address, but it no longer holds `DEFAULT_ADMIN_ROLE`. Every `hasRole(DEFAULT_ADMIN_ROLE, ...)` check fails permanently. There is no recovery path.

This can happen accidentally (e.g., admin testing the mechanism) or maliciously (a compromised key griefing the protocol).

**Impact:** Permanent loss of all `DEFAULT_ADMIN_ROLE`-gated functions: upgrading contracts, role management, setting exchange/treasury addresses. Protocol becomes permanently non-upgradeable and unmanageable.

**Recommended Mitigation:** Add a self-proposal guard in `proposeAdmin`:

```solidity
require(newAdmin != admin, "cannot self-propose");
```

**Myriad:** Fixed in commit [`3b4311d`](https://github.com/Polkamarkets/polkamarkets-js/commit/3b4311db173a492be10cf6b83f19f85699e9d064)

**Cyfrin:** Verified.
