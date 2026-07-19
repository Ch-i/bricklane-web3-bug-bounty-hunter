---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: '`BenqiEcosystemModule` and `UnifiedBudgetAllocator` are not fully ERC-165
  compliant'
vuln_class: []
---

# `BenqiEcosystemModule` and `UnifiedBudgetAllocator` are not fully ERC-165 compliant

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The `BenqiEcosystemModule` contract inherits both `IDistributionModule` and `IBenqiEcosystemModuleErrors`. According to the ERC-165 specification for interface detection, the `supportsInterface()` function should return `true` for every interface the contract implements. However, the current implementation only checks for `type(IDistributionModule).interfaceId` and the interfaces supported by the parent `ERC165` contract – it fails to include a check for `type(IBenqiEcosystemModuleErrors).interfaceId`.

The `UnifiedBudgetAllocator` contract similarly inherits from multiple interfaces, including `IBudgetAllocator`, `IUnifiedBudgetAllocatorEventsAndErrors`, and `UUPSUpgradeable` which implements `IERC1822Proxiable`. The `supportsInterface()` function is again incomplete since it only returns `true` for `IBudgetAllocator` and `IERC165`, failing to report its support for `IUnifiedBudgetAllocatorEventsAndErrors` and `IERC1822Proxiable`.

**Impact:** External contracts or off-chain tools that use ERC-165 for interface detection will incorrectly conclude that the `BenqiEcosystemModule` contract does not support the `IBenqiEcosystemModuleErrors` interface and the `UnifiedBudgetAllocator` contract does not support the `IUnifiedBudgetAllocatorEventsAndErrors` or `IERC1822Proxiable` interfaces. This can lead to failed integrations or misbehaving interactions with other systems that rely on proper interface discovery. While the core contract logic remains unaffected, this breaks compliance with the standard and can cause issues with composability and discoverability.

**Recommended Mitigation:** Modify the `supportsInterface()` functions to include checks for all implemented interfaces.

```solidity
// BenqiEcosystemModule.sol
function supportsInterface(bytes4 _interfaceId) public view virtual override returns (bool) {
    return
        _interfaceId == type(IDistributionModule).interfaceId ||
        _interfaceId == type(IBenqiEcosystemModuleErrors).interfaceId ||
        super.supportsInterface(_interfaceId);
}

// UnifiedBudgetAllocator.sol
function supportsInterface(bytes4 interfaceId) public view virtual override(DaoAuthorizableUpgradeable, IERC165) returns (bool) {
    return
        interfaceId == type(IBudgetAllocator).interfaceId ||
        interfaceId == type(IUnifiedBudgetAllocatorEventsAndErrors).interfaceId ||
        interfaceId == type(IERC1822Proxiable).interfaceId ||
        interfaceId == type(IERC165).interfaceId ||
}
```

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.
