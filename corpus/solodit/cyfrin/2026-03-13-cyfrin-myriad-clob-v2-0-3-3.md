---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`AdminRegistry::acceptAdmin` leaves other roles on the outgoing admin'
vuln_class: []
---

# `AdminRegistry::acceptAdmin` leaves other roles on the outgoing admin

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** When the pending admin calls `AdminRegistry::acceptAdmin`, we revoke `DEFAULT_ADMIN_ROLE` from the previous admin and grant it to the new admin. However, the outgoing admin may have granted themselves other protocol roles, `MARKET_ADMIN_ROLE`, `OPERATOR_ROLE`, `FEE_ADMIN_ROLE`, or `RESOLUTION_ADMIN_ROLE`, while they held `DEFAULT_ADMIN_ROLE`, which are not revoked in `acceptAdmin`.

The result is that after a handoff, the old admin retains any non-default roles they had assigned to themselves. This is inconsistent with the intent of a full admin transition and can leave the former admin with operational privileges (e.g. market or resolution admin) that the new admin may not expect.

```solidity
function acceptAdmin() external {
    require(msg.sender == pendingAdmin, "not pending admin");
    address oldAdmin = admin;
    _grantRole(DEFAULT_ADMIN_ROLE, pendingAdmin);
    _revokeRole(DEFAULT_ADMIN_ROLE, oldAdmin);
    admin = pendingAdmin;
    pendingAdmin = address(0);
    emit AdminAccepted(admin, oldAdmin);
}
```

**Recommended Mitigation:** Consider revoking all roles from the old admin when `acceptAdmin` completes. For example, explicitly revoke each protocol role from `oldAdmin` before updating state:

```solidity
_revokeRole(DEFAULT_ADMIN_ROLE, oldAdmin);
_revokeRole(MARKET_ADMIN_ROLE, oldAdmin);
_revokeRole(OPERATOR_ROLE, oldAdmin);
_revokeRole(FEE_ADMIN_ROLE, oldAdmin);
_revokeRole(RESOLUTION_ADMIN_ROLE, oldAdmin);
```

**Myriad:** Fixed in commit [`b2fc41f`](https://github.com/Polkamarkets/polkamarkets-js/commit/b2fc41fb0b3ff7f569bfabae8d06ed0becbcbb93)

**Cyfrin:** Verified.
