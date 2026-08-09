---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Duplicated validation in `DistributionManager::initialize` can be removed
vuln_class: []
---

# Duplicated validation in `DistributionManager::initialize` can be removed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** `DistributionManager::initialize` will revert if the `_initialBudgetAllocator` is equal to `address(0)`; however, this logic is not necessary as it is duplicated and already present in `_setBudgetAllocator()`.

```solidity
function initialize(
    ...
    IBudgetAllocator _initialBudgetAllocator,
    ...
) external initializer {
    if (address(_initialBudgetAllocator) == address(0))
        revert InvalidAddress("budgetAllocator");
    ...
    _setBudgetAllocator(_initialBudgetAllocator);
    ...
}

function _setBudgetAllocator(IBudgetAllocator _budgetAllocator) internal {
    if (address(_budgetAllocator) == address(0)) revert InvalidAddress("budgetAllocator");
    ...
}
```

**BENQI:** Fixed in PR [\#38](https://github.com/aragon/benqi-governance/pull/38).

**Cyfrin:** Verified.
