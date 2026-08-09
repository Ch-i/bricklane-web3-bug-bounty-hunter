---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Obsolete comments in `PositionManager`'
vuln_class: []
---

# [FIXED] Obsolete comments in `PositionManager`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[PositionManager.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/managers/PositionManager.sol#L98 "/contracts/main/managers/PositionManager.sol" "/contracts/main/managers/PositionManager.sol") | contract `PositionManager` > function `allowManagePosition` | 98

##### Description
In the contract `PositionManager`, the comment for the function `allowManagePosition` suggests obsolete typing for the `_ok` parameter, which is of `bool` type.
##### Recommendation
We recommend fixing the comment to match the variable type.
##### Update
###### Client's response
Fixed in commit [`5fe984f2ed654ae9c4621ca4dddbbbe8c04ca936`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/5fe984f2ed654ae9c4621ca4dddbbbe8c04ca936).
Fixed as suggested.
