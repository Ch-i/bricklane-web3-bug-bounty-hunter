---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: '`Getters::getCollateralSurplus` returns positive values even when `Surplus::processSurplus`
  is guaranteed to revert'
vuln_class: []
---

# `Getters::getCollateralSurplus` returns positive values even when `Surplus::processSurplus` is guaranteed to revert

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** The view function `Getters::getCollateralSurplus` computes and returns a positive surplus value for a collateral **even when the global collateral ratio is below the `surplusBufferRatio`**.

However, function `Surplus::processSurplus` **always reverts** in this situation due to the explicit check:
```solidity
  function processSurplus(
    ...
  )
    ...
  {
    ...
    (uint64 collatRatio,,,,) = LibGetters.getCollateralRatio();
@>  if (collatRatio < ts.surplusBufferRatio) revert Undercollateralized();
    emit SurplusProcessed(collateralSurplus, stableSurplus, issuedAmount);
  }
```

This means that whenever the global system is under-buffered (i.e., `collatRatio < surplusBufferRatio`), any call to `Surplus::processSurplus` that was triggered after reading a positive value from `Getters::getCollateralSurplus` will revert.

**Recommended Mitigation:** Consider documenting this behavior: A positive return from `Getters::getCollateralSurplus` **does not** guarantee that `Surplus::processSurplus` will succeed — the global collateral ratio must still be ≥ surplusBufferRatio.

Optionally, consider introducing a custom error (i.e. `SurplusNotProcessable`) in the `Getters::getCollateralSurplus` function for explicit signaling that surplus can't be processed because the system is below the defined `surplusBufferRatio`.

**Parallel:** Fixed in commit [60fec2c](https://github.com/parallel-protocol/parallel-parallelizer/commit/60fec2cba723dc47984d3b8b8e000cb5c86c3073)

**Cyfrin:** Verified. `LibSurpluss::_computeCollateralSurplus` now reverts if `collateralRatio < surplusBufferRatio`.
