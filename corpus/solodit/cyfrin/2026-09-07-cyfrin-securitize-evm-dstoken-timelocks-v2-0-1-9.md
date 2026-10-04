---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-9
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: '`TrustService::removeRole` on an address with no role emits DSTrustServiceRoleAdded'
vuln_class: []
---

# `TrustService::removeRole` on an address with no role emits DSTrustServiceRoleAdded

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `TrustService::setRoleImpl` picks the event from the previous stored role: `old_role == NONE` emits `DSTrustServiceRoleAdded`, otherwise `DSTrustServiceRoleRemoved`. `TrustService::removeRole` only checks `role != MASTER`, so calling it on an address whose role is already `NONE` passes, rewrites `NONE` to `NONE`, and emits `DSTrustServiceRoleAdded(_address, NONE, msg.sender)` for a call that removed nothing.

**Impact:** Storage is unchanged. Off-chain indexers that rebuild the role table from events record a spurious "role granted: NONE" entry, and MASTER or the roles governor, the only callers that pass `onlySameRoleForAddress` on an address with no role, can repeat this on any address.

**Recommended Mitigation:** Reject removal of a role that is not set:

```solidity
function removeRole(address _address) public override onlyRoleAdmin onlySameRoleForAddress(_address) returns (bool) {
    uint8 role = roles[_address];
    require(role != NONE, "Address has no role to remove");
    require(role != MASTER, "Cannot remove master");
    setRoleImpl(_address, NONE);
    return true;
}
```

**Securitize:** Acknowledged.
