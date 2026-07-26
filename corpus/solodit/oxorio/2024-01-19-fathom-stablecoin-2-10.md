---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-10
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Outdated typing in `FixedSpreadLiquidationStrategy`'
vuln_class: []
---

# [FIXED] Outdated typing in `FixedSpreadLiquidationStrategy`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FixedSpreadLiquidationStrategy.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol#L56 "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol" "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol") | contract `FixedSpreadLiquidationStrategy` | 56
[FixedSpreadLiquidationStrategy.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol#L143 "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol" "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol") | contract `FixedSpreadLiquidationStrategy` > function `setFlashLendingEnabled` | 143

##### Description
In the `FixedSpreadLiquidationStrategy` contract, the `flashLendingEnabled` variable is incorrectly defined as `uint256` instead of the appropriate `bool` type.

The same issue exists in the [`setFlashLendingEnabled`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol#L143 "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol") function, where the parameter `_flashLendingEnabled` is erroneously defined as `uint256`.
##### Recommendation
We recommend changing the variable type to `bool`.
##### Update
###### Client's response
Fixed in commit [`11066b49d5b632a66b495d437031c6969b65558f`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/11066b49d5b632a66b495d437031c6969b65558f).
Fixed as suggested

`flashLendingEnabled` from `uint` to `bool`.
event, function, execute fn's subroutine all changed accordingly.
