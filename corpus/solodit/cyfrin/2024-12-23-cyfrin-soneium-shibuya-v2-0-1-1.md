---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-23-cyfrin-soneium-shibuya-v2-0-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-12-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-23-cyfrin-soneium-shibuya-v2-0
title: Redundant owner-based access control implementation
vuln_class: []
---

# Redundant owner-based access control implementation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-23-cyfrin-soneium-shibuya-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md)_

---

**Description:** The contract implements a custom ownership system alongside `AccessControlUpgradeable`, but fails to utilize the latter's built-in access control mechanisms effectively. Since the owner is not granted the `DEFAULT_ADMIN_ROLE`, the contract is forced to override several public functions from `AccessControlUpgradeable` to maintain proper access control.

This design choice implies potential issues:
1. Unnecessarily duplicates access control functionality that already exists in `AccessControlUpgradeable`
2. Requires overriding `grantRole()` and `revokeRole()` functions
3. Inconsistently handles role management by missing the override for `renounceRole()`
4. Increases code complexity and potential for access control confusion

While the current implementation is functional, it introduces unnecessary complexity and potential maintenance challenges.

**Recommended Mitigation:** Instead of implementing a separate ownership system we recommend the team to consider:
1. Grant the `DEFAULT_ADMIN_ROLE` to the owner during initialization
2. Remove custom ownership implementation
3. Utilize `AccessControlUpgradeable`'s built-in role management functions
4. Remove unnecessary function overrides

**Startale:** Acknowledged.

**Cyfrin:** Acknowledged.
