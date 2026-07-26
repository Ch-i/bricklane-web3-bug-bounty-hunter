---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-10
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] `Address` imported instead of `AddressUpgradeable` in `BookKeeper`'
vuln_class: []
---

# [FIXED] `Address` imported instead of `AddressUpgradeable` in `BookKeeper`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[BookKeeper.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/BookKeeper.sol#L6 "/contracts/main/stablecoin-core/BookKeeper.sol" "/contracts/main/stablecoin-core/BookKeeper.sol") | None | 6

##### Description
In the contract `BookKeeper`, the `Address` contract is imported, while other OpenZeppelin imports use the upgradeable version of the contracts.
##### Recommendation
We recommend importing the `AddressUpgradeable` contract to unify imports.
##### Update
###### Client's response
Fixed in commit [`08eeb18486d2fe95ea5e06d4383e5f817b0fba45`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/08eeb18486d2fe95ea5e06d4383e5f817b0fba45).
Fixed as suggested.
