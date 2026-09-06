---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Redundant Imports'
vuln_class: []
---

# [FIXED] Redundant Imports

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[PositionManager.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/managers/PositionManager.sol#L9 "/contracts/main/managers/PositionManager.sol" "/contracts/main/managers/PositionManager.sol") | contract `PositionManager` | 9
[CentralizedOraclePriceFeed.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/price-feeders/CentralizedOraclePriceFeed.sol#L6 "/contracts/main/price-feeders/CentralizedOraclePriceFeed.sol" "/contracts/main/price-feeders/CentralizedOraclePriceFeed.sol") | contract `CentralizedOraclePriceFeed` | 6
[SlidingWindowDexOracle.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/price-oracles/SlidingWindowDexOracle.sol#L8 "/contracts/main/price-oracles/SlidingWindowDexOracle.sol" "/contracts/main/price-oracles/SlidingWindowDexOracle.sol") | contract `SlidingWindowDexOracle` | 8
[FathomStablecoinProxyActions.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol#L11 "contracts/main/proxy-actions/FathomStablecoinProxyActions.sol" "/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol") | contract `FathomStablecoinProxyActions` | 11
[FathomStablecoinProxyActions.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol#L12 "contracts/main/proxy-actions/FathomStablecoinProxyActions.sol" "/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol") | contract `FathomStablecoinProxyActions` | 12
[CollateralTokenAdapter.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/adapters/CollateralTokenAdapter/CollateralTokenAdapter.sol#L10 "/contracts/main/stablecoin-core/adapters/CollateralTokenAdapter/CollateralTokenAdapter.sol" "/contracts/main/stablecoin-core/adapters/CollateralTokenAdapter/CollateralTokenAdapter.sol") | contract `CollateralTokenAdapter` | 10
[AdminControls.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/AdminControls.sol#L7 "/contracts/main/stablecoin-core/AdminControls.sol" "/contracts/main/stablecoin-core/AdminControls.sol") | contract `AdminControls` | 7
[ShowStopper.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/ShowStopper.sol#L12 "/contracts/main/stablecoin-core/ShowStopper.sol" "/contracts/main/stablecoin-core/ShowStopper.sol") | contract `ShowStopper` | 12
[SystemDebtEngine.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/SystemDebtEngine.sol#L9 "/contracts/main/stablecoin-core/SystemDebtEngine.sol" "/contracts/main/stablecoin-core/SystemDebtEngine.sol") | contract `SystemDebtEngine` | 9

##### Description
There are redundant imports in the mentioned locations.
##### Recommendation
We recommend removing redundant imports to keep the codebase clean.
##### Update
###### Client's response
Fixed in commit [`d4f064853cd9c1085d0fd74ebedfdeb5df3a2903`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/d4f064853cd9c1085d0fd74ebedfdeb5df3a2903).
Fixed as suggested.
