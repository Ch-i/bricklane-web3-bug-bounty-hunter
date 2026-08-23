---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: '`BaseDelegator` is not using upgradeable version of `ERC165`'
vuln_class: []
---

# `BaseDelegator` is not using upgradeable version of `ERC165`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `BaseDelegator` contract currently inherits from the non-upgradeable version of ERC165. This could limit the contract's ability to adapt to future upgrades or modifications of the ERC165 interface, potentially impacting the contract's upgradability and compatibility with other upgradeable contracts. This can lead to issues, as the non-upgradeable version does not have the necessary initializers and storage gap reserved for upgradeable contracts.

**Impact:** Using the non-upgradeable `ERC165` in an otherwise upgradeable contract (`BaseDelegator`) introduces a risk of incompatibility with future upgrades.

**Recommended Mitigation:** Make the following change to the `BaseDelagator`
```diff
- abstract contract BaseDelegator is AccessControlUpgradeable, ReentrancyGuardUpgradeable, IBaseDelegator, ERC165 {
+ abstract contract BaseDelegator is AccessControlUpgradeable, ReentrancyGuardUpgradeable, IBaseDelegator, ERC165Upgradeable {
    using ERC165Checker for address;
```

**Suzaku:**
Acknowledged.

**Cyfrin:** Acknowledged.
