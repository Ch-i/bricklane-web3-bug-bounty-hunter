---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: '`collatInfo.stablecoinCap` hardcap can be bypassed via `SettersGovernor::adjustStablecoins`'
vuln_class: []
---

# `collatInfo.stablecoinCap` hardcap can be bypassed via `SettersGovernor::adjustStablecoins`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** The `stablecoinCap` parameter in the `Collateral` struct is intended to cap the maximum amount of normalized stablecoins (`normalizedStables`) that a single collateral asset can back. This limit is correctly enforced during normal user mint operations in the `Swapper` facet.

However, the Governor can call `SettersGovernor::adjustStablecoins` to arbitrarily **increase** `normalizedStables` **without any check** against `stablecoinCap`. This creates a direct bypass of the hardcap mechanism, allowing the system to enter a state where a collateral backs more stablecoins than its configured limit.

**Proof of Concept:** Missing cap validation in the increase path of `LibSetters::adjustStablecoins`:

```solidity
// `LibSetters::adjustStablecoins`
if (increase) {
    newCollateralNormalizedStable += uint216(normalizedAmount);
    newNormalizedStables += uint216(normalizedAmount);
    // Missing:
    // if (newCollateralNormalizedStable * ts.normalizer / BASE_27 > collatInfo.stablecoinCap) revert AboveCap();
}
```

**Recommended Mitigation:** Add cap enforcement in the increase path:
```diff
// In LibSetters.adjustStablecoins
if (increase) {
    newCollateralNormalizedStable += uint216(normalizedAmount);
    newNormalizedStables += uint216(normalizedAmount);

+   if (newCollateralNormalizedStable * ts.normalizer / BASE_27 > collatInfo.stablecoinCap) {
+       revert AboveCap();
+   }
}
```

**Parallel**
Fixed in commit [7df01b8](https://github.com/parallel-protocol/parallel-parallelizer/commit/7df01b8df43f32dabf1e5dcf19ebe6ae2f9060d3#diff-41e3c405851499899c192341a0bd4b5587ba64730ba738b5db5ebba0a08de5c2) && commit [f41738d](https://github.com/parallel-protocol/parallel-parallelizer/commit/f41738d754a541a06aef4fd9037bc9b1fd08b755)

**Cyfrin:** Verified. Implemented a check to validate that `stablecoinCap` is not bypassed.
