---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-4-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: '`bondFaceValue` read in `PerpetualBond::_convertToBond` can be cached'
vuln_class: []
---

# `bondFaceValue` read in `PerpetualBond::_convertToBond` can be cached

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** The storage value `bondFaceValue` is read twice in [`PerpetualBond::__convertToBond`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L291-L294):
```solidity
function _convertToBond(uint256 assetAmount) internal view returns (uint256) {
    if (bondFaceValue == 0) return 0; // Prevent division by zero
    return (assetAmount * 1e18) / bondFaceValue;
}
```
The value can be cached and only read once:
```solidity
function _convertToBond(uint256 assetAmount) internal view returns (uint256) {
    // cache read
    uint256 _bondFaceValue = bondFaceValue;
    if (_bondFaceValue == 0) return 0; // Prevent division by zero
    return (assetAmount * 1e18) / _bondFaceValue;
}
```

**YieldFi:** Fixed in commit [`823b010`](https://github.com/YieldFiLabs/contracts/commit/823b010d74fd55fb88b31619c1a94dac2ef65ad3)

**Cyfrin:** Verified.
