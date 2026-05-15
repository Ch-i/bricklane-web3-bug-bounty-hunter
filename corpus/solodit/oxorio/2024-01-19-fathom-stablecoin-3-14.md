---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-14
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Typo in several contracts'
vuln_class: []
---

# [FIXED] Typo in several contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[IDelayPriceFeed.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/interfaces/IDelayPriceFeed.sol#L23 "/contracts/main/interfaces/IDelayPriceFeed.sol" "/contracts/main/interfaces/IDelayPriceFeed.sol") | interface `IDelayPriceFeed` | 23
[CentralizedOraclePriceFeed.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/price-feeders/CentralizedOraclePriceFeed.sol#L33 "/contracts/main/price-feeders/CentralizedOraclePriceFeed.sol" "/contracts/main/price-feeders/CentralizedOraclePriceFeed.sol") | contract `CentralizedOraclePriceFeed` | 33
[DelayFathomOraclePriceFeed.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/price-feeders/DelayFathomOraclePriceFeed.sol#L54 "/contracts/main/price-feeders/DelayFathomOraclePriceFeed.sol" "/contracts/main/price-feeders/DelayFathomOraclePriceFeed.sol") | contract `DelayFathomOraclePriceFeed` | 54
[DelayPriceFeedBase.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/price-feeders/DelayPriceFeedBase.sol#L73 "/contracts/main/price-feeders/DelayPriceFeedBase.sol" "/contracts/main/price-feeders/DelayPriceFeedBase.sol") | contract `DelayPriceFeedBase` > function `peekPrice` | 73
[DelayPriceFeedBase.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/price-feeders/DelayPriceFeedBase.sol#L103 "/contracts/main/price-feeders/DelayPriceFeedBase.sol" "/contracts/main/price-feeders/DelayPriceFeedBase.sol") | contract `DelayPriceFeedBase` | 103

##### Description
In mentioned locations “retrive” in the names of functions should be replaced with “retrieve”.
##### Recommendation
We recommend fixing the typo.
##### Update
###### Client's response
Fixed in commit [`aab9f1a307e3d8e238f54913a350ca74bcba446c`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/aab9f1a307e3d8e238f54913a350ca74bcba446c).
Fixed as suggested.
