---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Casting to types in unsafe way'
vuln_class: []
---

# [FIXED] Casting to types in unsafe way

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[CollateralTokenAdapter.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/adapters/CollateralTokenAdapter/CollateralTokenAdapter.sol#L189 "/contracts/main/stablecoin-core/adapters/CollateralTokenAdapter/CollateralTokenAdapter.sol" "/contracts/main/stablecoin-core/adapters/CollateralTokenAdapter/CollateralTokenAdapter.sol") | contract `CollateralTokenAdapter` > function `_deposit` | 189

##### Description
In these locations, there are casts to the `int256` and `uint256` types. In some cases, there are validations to prevent overflow, while in other locations, any checks are missing.
##### Recommendation
We recommend unifying the handling of casting to `int256` by utilizing `safeToInt256` and `safeToUint256` functions in all places, validating scenarios when the variable can overflow/underflow.
##### Update
###### Client's response
Fixed in commit [`e368d26bf75e871e983bbd7bd60f446e92ce2396`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/e368d26bf75e871e983bbd7bd60f446e92ce2396).
Fixed as suggested. 

Added `safeToInt256` and `safeToUint256` to the type casting in contracts. Left `CollateralTokenAdapter`'s casting with overflow/underflow check as is.
