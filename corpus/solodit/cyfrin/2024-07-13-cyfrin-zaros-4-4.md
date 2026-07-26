---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Optimize away call to `EnumerableSet::contains` in `GlobalConfiguration::configureCollateralLiquidationPriority`
vuln_class: []
---

# Optimize away call to `EnumerableSet::contains` in `GlobalConfiguration::configureCollateralLiquidationPriority`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Optimize away call to `EnumerableSet::contains` in `GlobalConfiguration::configureCollateralLiquidationPriority` by using the `bool` result from `EnumerableSet::add`.

**Recommended Mitigation:**
```solidity
function configureCollateralLiquidationPriority(Data storage self, address[] memory collateralTypes) internal {
    for (uint256 i = 0; i < collateralTypes.length; i++) {
        if (collateralTypes[i] == address(0)) {
            revert Errors.ZeroInput("collateralType");
        }

        if(!self.collateralLiquidationPriority.add(collateralTypes[i])) {
            revert Errors.MarginCollateralAlreadyInPriority(collateralTypes[i]);
        }
    }
}
```

**Zaros:** Fixed in commit [5b8e51e](https://github.com/zaros-labs/zaros-core/commit/5b8e51e39d8f052480af31b490404e29ad34335f#diff-3d4f0f7ecf19ca9cf461570d8c3f5ac0ba6b60345386d9ebf0d820e7c997738dL103-L107).

**Cyfrin:** Verified.
