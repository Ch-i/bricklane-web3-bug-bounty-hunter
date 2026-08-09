---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Missing interface compliance validation in `DistributorManager`
vuln_class: []
---

# Missing interface compliance validation in `DistributorManager`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The `DistributionManager` contract does not currently validate that the `budgetAllocator` and controller module contracts implement the required interfaces when set during initialization or via `setBudgetAllocator()` and `setModuleForController()` respectively. Both the `UnifiedBudgetAllocator` and `BenqiCoreModule` contracts implement `ERC165::supportsInterface` to declare interface compliance; however, the setter functions do not verify this before accepting the contracts as valid.

```solidity
// DistributionManager.sol
function _setBudgetAllocator(IBudgetAllocator _budgetAllocator) internal {
    if (address(_budgetAllocator) == address(0)) revert InvalidAddress("budgetAllocator");

    // @audit -  missing interface validation check

    address oldAllocator = address(budgetAllocator);
    budgetAllocator = _budgetAllocator;

    emit BudgetAllocatorSet(oldAllocator, address(_budgetAllocator));
}

function _setModuleForController(
    address _rewardController,
    IDistributionModule _module
) internal {
    if (_rewardController == address(0)) revert InvalidAddress("rewardController");
    if (address(_module) == address(0)) revert InvalidAddress("module");

    // @audit -  missing interface validation check

    if (address(rewardControllerToModule[_rewardController]) != address(0)) {
        revert ControllerAlreadyRegistered(_rewardController);
    }

    _activeRewardControllers.add(_rewardController);
    rewardControllerToModule[_rewardController] = _module;

    emit ModuleForControllerSet(_rewardController, address(_module));
}
```

**Impact:** Setting an incompatible contract would completely DoS the distribution system.

**Recommended Mitigation:** Add ERC-165 interface validation checks to both setter functions:

```soldity
if (!IERC165(address(_budgetAllocator)).supportsInterface(type(IBudgetAllocator).interfaceId)) {
      revert InvalidInterface("budgetAllocator");
}
```

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.
