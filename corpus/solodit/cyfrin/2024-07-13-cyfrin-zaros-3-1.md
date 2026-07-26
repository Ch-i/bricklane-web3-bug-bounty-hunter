---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Return more suitable error type when `params.initialMarginRateX18 <= params.maintenanceMarginRateX18`
vuln_class: []
---

# Return more suitable error type when `params.initialMarginRateX18 <= params.maintenanceMarginRateX18`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** In `GlobalConfigurationBranch::createPerpMarket`, the following two error cases both return the `ZeroInput` error type:
```solidity
if (params.initialMarginRateX18 <= params.maintenanceMarginRateX18) {
    revert Errors.ZeroInput("initialMarginRateX18");
}
if (params.initialMarginRateX18 == 0) {
    revert Errors.ZeroInput("initialMarginRateX18");
}
```

In the first case where `initialMarginRateX18 < maintenanceMarginRateX18` the error is misleading; a more suitable error type such as `InvalidParameter` should be returned.

The same occurs in `GlobalConfigurationBranch::updatePerpMarketConfiguration` but there the second check `initialMarginRateX18 == 0` is omitted; consider whether to add this check in.

The second validation may be redundant because the first validation will always revert first; if a specific error is desired for the zero case then perform it first, otherwise consider removing it.

**Zaros:** Fixed in commit [c35e2be](https://github.com/zaros-labs/zaros-core/commit/c35e2bea50a0753726ac79503e607e9dcf637b6b).

**Cyfrin:** Verified.
