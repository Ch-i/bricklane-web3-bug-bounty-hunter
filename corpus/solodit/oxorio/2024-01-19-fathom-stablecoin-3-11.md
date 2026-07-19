---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-11
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Typo in error message in `FixedSpreadLiquidationStrategy`'
vuln_class: []
---

# [FIXED] Typo in error message in `FixedSpreadLiquidationStrategy`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FixedSpreadLiquidationStrategy.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol#L165 "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol" "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol") | contract `FixedSpreadLiquidationStrategy` > function `execute` | 165

##### Description
In the function `execute` of the contract `FixedSpreadLiquidationStrategy`, the error message contains a typo - `liquidationEngingRole`.
##### Recommendation
We recommend replacing the error message with `LIQUIDATION_ENGINE_ROLE`.
##### Update
###### Client's response
Fixed in commit [`55e02025dcfc9a0e90deb5b1d6ba644e07452a1a`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/55e02025dcfc9a0e90deb5b1d6ba644e07452a1a).
Fixed as suggested.
