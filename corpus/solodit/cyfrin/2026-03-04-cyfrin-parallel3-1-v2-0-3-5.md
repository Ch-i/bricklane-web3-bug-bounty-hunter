---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Unbounded `O(n)` renormalization in `_updateNormalizer` can lead to denial-of-service
  during redemption
vuln_class: []
---

# Unbounded `O(n)` renormalization in `_updateNormalizer` can lead to denial-of-service during redemption

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** The function `Redeemer::_updateNormalizer` contains a renormalization loop that iterates over **all collaterals** (`ts.collateralList`) and performs storage writes when the computed `newNormalizerValue` falls outside the safe precision range `[BASE_18, BASE_36)`:

```solidity
if (newNormalizerValue <= BASE_18 || newNormalizerValue >= BASE_36) {
    address[] memory collateralListMem = ts.collateralList;
    uint256 collateralListLength = collateralListMem.length;
    uint128 newNormalizedStables;
    for (uint256 i; i < collateralListLength; ++i) {
        uint128 newCollateralNormalizedStable = (
            (uint256(ts.collaterals[collateralListMem[i]].normalizedStables) * newNormalizerValue) / BASE_27
        ).toUint128();
        newNormalizedStables += newCollateralNormalizedStable;
        ts.collaterals[collateralListMem[i]].normalizedStables = uint216(newCollateralNormalizedStable);
    }
    ts.normalizedStables = newNormalizedStables;
    newNormalizerValue = BASE_27;
}
```

The renormalization is a precision-protection mechanism that rescales all per-collateral `normalizedStables` values when drift becomes extreme. While the design intent is sound, performing this O(n) operation synchronously within a public, unrestricted user function creates a theoretical gas griefing vector that could cause a DoS on redemptions.


**Recommended Mitigation:** Introduce a governance-settable `maxCollateralCount` variable with a sane default, and enforce it in `LibSetters::addCollateral`.

**Parallel:** Acknowledged
