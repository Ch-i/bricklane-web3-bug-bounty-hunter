---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[NO ISSUE] Validation of `_totalDebtCeiling` in `BookKeeper`'
vuln_class: []
---

# [NO ISSUE] Validation of `_totalDebtCeiling` in `BookKeeper`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[BookKeeper.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/BookKeeper.sol#L150 "/contracts/main/stablecoin-core/BookKeeper.sol" "/contracts/main/stablecoin-core/BookKeeper.sol") | contract `BookKeeper` > function `setTotalDebtCeiling` | 150

##### Description
In the function [`setTotalDebtCeiling`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/BookKeeper.sol#L150 "/contracts/main/stablecoin-core/BookKeeper.sol") of the contract `BookKeeper`, the `_totalDebtCeiling` parameter must be passed in rad, which is not enforced. Incorrect variable passed will lead to the failed calls of the `adjustPosition` transactions in the `BookKeeper`.
##### Recommendation
We recommend validating the parameter to be passed in rad.
##### Update
###### Client's response
Fix no need. 
The `debtCeiling` can be theoretically 0.5 FXD, which is below 1 `RAD` of debt ceiling.
