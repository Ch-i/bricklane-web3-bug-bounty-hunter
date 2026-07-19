---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Ownership can be transferred to a restricted address
vuln_class: []
---

# Ownership can be transferred to a restricted address

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** `sUSBD` prevents restricting the current `owner()` and `treasury` in `sUSBD::setRestrictedStatus`, and it also prevents setting `treasury` to an address with a non-`NONE` restricted status in `sUSBD::setTreasury`.

However, there is no equivalent guard on ownership changes: the owner can transfer ownership to an address that is already restricted (e.g., `SOFT/HARD/FULL`). If that happens, the restriction on the new owner cannot be lifted via `setRestrictedStatus`, because `setRestrictedStatus` explicitly rejects updates when `account == owner()`. As a result, the only way to “unrestrict” that owner address would be to transfer ownership again to a different (non-restricted) address.

Consider overriding/guarding the ownership transfer flow (e.g., `transferOwnership`) to require `restrictedStatuses[newOwner] == RestrictedStatus.NONE`, aligning ownership changes with the protocol’s restriction policy.


**Boundary:**
Acknowledged. Restriction status does not affect administrative operations, so additional guards are unnecessary.

\clearpage
