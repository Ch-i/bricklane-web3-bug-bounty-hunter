---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Redundant check for `totalStablecoinIssued` in multiple contracts'
vuln_class: []
---

# [FIXED] Redundant check for `totalStablecoinIssued` in multiple contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[PositionManager.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/managers/PositionManager.sol#L333 "/contracts/main/managers/PositionManager.sol" "/contracts/main/managers/PositionManager.sol") | contract `PositionManager` > function `setBookKeeper` | 333
[PositionManager.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/managers/PositionManager.sol#L85 "/contracts/main/managers/PositionManager.sol" "/contracts/main/managers/PositionManager.sol") | contract `PositionManager` > function `initialize` | 85
[FixedSpreadLiquidationStrategy.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol#L110 "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol" "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol") | contract `FixedSpreadLiquidationStrategy` > function `initialize` | 110
[FixedSpreadLiquidationStrategy.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol#L258 "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol" "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol") | contract `FixedSpreadLiquidationStrategy` > function `setBookKeeper` | 258
[LiquidationEngine.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/LiquidationEngine.sol#L95 "/contracts/main/stablecoin-core/LiquidationEngine.sol" "/contracts/main/stablecoin-core/LiquidationEngine.sol") | contract `LiquidationEngine` > function `initialize` | 95
[LiquidationEngine.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/LiquidationEngine.sol#L212 "/contracts/main/stablecoin-core/LiquidationEngine.sol" "/contracts/main/stablecoin-core/LiquidationEngine.sol") | contract `LiquidationEngine` > function `setBookKeeper` | 212
[PriceOracle.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/PriceOracle.sol#L84 "/contracts/main/stablecoin-core/PriceOracle.sol" "/contracts/main/stablecoin-core/PriceOracle.sol") | contract `PriceOracle` > function `setBookKeeper` | 84
[PriceOracle.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/PriceOracle.sol#L77 "/contracts/main/stablecoin-core/PriceOracle.sol" "/contracts/main/stablecoin-core/PriceOracle.sol") | contract `PriceOracle` > function `initialize` | 77
[ShowStopper.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/ShowStopper.sol#L65 "/contracts/main/stablecoin-core/ShowStopper.sol" "/contracts/main/stablecoin-core/ShowStopper.sol") | contract `ShowStopper` > function `initialize` | 65
[ShowStopper.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/ShowStopper.sol#L72 "/contracts/main/stablecoin-core/ShowStopper.sol" "/contracts/main/stablecoin-core/ShowStopper.sol") | contract `ShowStopper` > function `setBookKeeper` | 72

##### Description
In the mentioned locations, the `require` statement that checks `totalStablecoinIssued >= 0` is redundant since `totalStablecoinIssued` is of type `uint256`.
##### Recommendation
We recommend removing the redundant check.
##### Update
###### Client's response
Fixed in commit [`f024a0f23a8ad9975a1651d6a5beb7dffef74629`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/f024a0f23a8ad9975a1651d6a5beb7dffef74629).
Fixed as suggested.
Redundant checks for `totalStablecoinIssued` in multiple contracts removed.
