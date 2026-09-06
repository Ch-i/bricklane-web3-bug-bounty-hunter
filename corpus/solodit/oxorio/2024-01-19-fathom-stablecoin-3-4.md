---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-4
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
title: '[ACKNOWLEDGED] Transfer amount validation in `FathomProxyWalletOwnerUpgradeable`'
vuln_class: []
---

# [ACKNOWLEDGED] Transfer amount validation in `FathomProxyWalletOwnerUpgradeable`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwnerUpgradeable.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L90 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") | contract `FathomProxyWalletOwnerUpgradeable` > function `openPosition` | 90

##### Description
In the function [`openPosition`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L90), the `msg.value` amount in the `FathomProxyWalletOwnerUpgradeable` contract is not validated to be non-zero. 
Same applies to the non-upgradeable version of the contract.
##### Recommendation
We recommend validating that `msg.value` is positive before performing any logic related to opening a position.
##### Update
###### Client's response
We would like to exclude `FathomProxyWalletOwner` and  `FathomProxyWalletOwnerUpgradeable`  from the audit scope.
