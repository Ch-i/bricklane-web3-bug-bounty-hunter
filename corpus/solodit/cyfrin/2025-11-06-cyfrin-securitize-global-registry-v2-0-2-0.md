---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Don't emit misleading events when roles haven't been added or revoked
vuln_class: []
---

# Don't emit misleading events when roles haven't been added or revoked

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `AccessControlUpgradeable::_grantRole` and `_revokeRole` [return](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/access/AccessControlUpgradeable.sol#L204-L231) `bool` to indicate whether the role was actually granted or revoked.

**Impact:** Some functions using these don't check the `bool` return then emit events; such events will be misleading if the roles were not actually granted or revoked.

**Recommended Mitigation:** The affected functions are:
* `GlobalRegistryService::changeAdmin, addOperator, revokeOperator`

In these functions check the return of `_grantRole` and `_revokeRole` and only emit events if the roles were actually granted or revoked.

**Securitize:** Fixed in commit [c7d50ac](https://github.com/securitize-io/bc-global-registry-service-sc/commit/c7d50acbe661aae0edd62e54c91692d3ff3a35b9).

**Cyfrin:** Verified.
