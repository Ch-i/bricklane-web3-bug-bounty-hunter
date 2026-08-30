---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] Redundant extension of the `AccessControl` contract to check two roles
  at once in `AccessControl2RolesValuation`'
vuln_class: []
---

# [FIXED] Redundant extension of the `AccessControl` contract to check two roles at once in `AccessControl2RolesValuation`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[AccessControl2RolesValuation.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/AccessControl2RolesValuation.sol#L6 "/contracts/AccessControl2RolesValuation.sol") | - | 6

##### Description
In the `AccessControl2RolesValuation` contract, the `only2Roles` modifier is introduced to check the permissions of two roles simultaneously, specifically for the pair `DEFAULT_ADMIN_ROLE` and `EMERGENCY_ROLE`.

However, the `DEFAULT_ADMIN_ROLE` is the primary administrative role with authority to assign other roles, including the `EMERGENCY_ROLE`. Thus, an admin with the `DEFAULT_ADMIN_ROLE` can assign the `EMERGENCY_ROLE` to themselves.

Consequently, using `only2Roles([DEFAULT_ADMIN_ROLE, EMERGENCY_ROLE])` becomes redundant and can be replaced with the simpler modifier `onlyRole(EMERGENCY_ROLE)`.

##### Recommendation
We recommend revisiting the use of the `only2Roles` modifier and considering the use of `onlyRole` for code simplification.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).
