---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Typo in `PositionManager`'
vuln_class: []
---

# [FIXED] Typo in `PositionManager`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[PositionManager.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/managers/PositionManager.sol#L255 "/contracts/main/managers/PositionManager.sol" "/contracts/main/managers/PositionManager.sol") | contract `PositionManager` | 255

##### Description
In the contract `PositionManager`, there is a typo in the comment in the word `addresss`.
##### Recommendation
We recommend fixing the typo to `address`.
##### Update
###### Client's response
Fixed in commit [`96a66f914b433d1535eee546ff3f1da80055e6d2`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/96a66f914b433d1535eee546ff3f1da80055e6d2).
Fixed as suggested.
