---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Potential for Zero Allocation in `updateAllocations` Function Without Validation
vuln_class: []
---

# Potential for Zero Allocation in `updateAllocations` Function Without Validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved

**Source**: PlaneToken.sol

**Description**:

The `updateAllocations` function allows the owner to update the allocations for farming and legacy holders. However, the function lacks validation to prevent either `farmingAllocation_` or `legacyAllocation_` from being set to zero. This oversight could lead to scenarios where one or both allocations are unintentionally set to zero, potentially disrupting the intended distribution of rewards and affecting the incentive mechanisms of the platform.

**Recommendation: **

To mitigate these issues and enhance the function's robustness, it is recommended to implement the following changes:

**Validation Checks:** Introduce validation checks to ensure that neither `farmingAllocation_` nor `legacyAllocation_` can be set to zero unless explicitly intended as part of the platform's strategy. This could involve requiring that each allocation is greater than a certain minimum threshold.

**Explicit Zero Allocation Handling**: If there are valid scenarios where an allocation might need to be set to zero, implement explicit handling and documentation for these cases to ensure that such actions are deliberate and well-understood.

**Adjustable Minimum Thresholds**: Consider implementing adjustable minimum thresholds for allocations that can be modified by the owner or through governance mechanisms. This allows for flexibility while still preventing accidental zero allocations.


```solidity
function updateAllocations(uint256 farmingAllocation_, uint256 legacyAllocation_) external onlyOwner {
    // apply emissions before changes
    emitAllocations();

    // total sum of allocations can't be > 100%
    uint256 totalAllocationsSet = farmingAllocation_.add(legacyAllocation_);
    require(totalAllocationsSet <= 100, "updateAllocations: total allocation is too high");

    // Ensure neither allocation is set to zero unintentionally
    require(farmingAllocation_ > 0 && legacyAllocation_ > 0, "updateAllocations: allocations must be greater than zero");

    // set new allocations
    farmingAllocation = farmingAllocation_;
    legacyAllocation = legacyAllocation_;

    emit UpdateAllocations(farmingAllocation_, legacyAllocation_, treasuryAllocation());
}


```
