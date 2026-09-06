---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[NO ISSUE] Validation of `_debtFloor` in `CollateralPoolConfig`'
vuln_class: []
---

# [NO ISSUE] Validation of `_debtFloor` in `CollateralPoolConfig`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[CollateralPoolConfig.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol#L118 "/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol" "/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol") | contract `CollateralPoolConfig` > function `setDebtFloor` | 118

##### Description
In the function [`setDebtFloor`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol#L118 "/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol") of the contract `CollateralPoolConfig`, the parameter `_debtFloor` must be passed in rad, which is not enforced.
##### Recommendation
We recommend validating the parameter to be passed in rad.
##### Update
###### Client's response
Fix no need. 
Position debt floor can theoretically be 0.5 FXD or even 0, when debt floor is not forced.
