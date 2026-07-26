---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-3
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
title: '[ACKNOWLEDGED] Received amount of stablecoin is not validated in `FathomProxyWalletOwnerUpgradeable`'
vuln_class: []
---

# [ACKNOWLEDGED] Received amount of stablecoin is not validated in `FathomProxyWalletOwnerUpgradeable`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwnerUpgradeable.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L91 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") | contract `FathomProxyWalletOwnerUpgradeable` > function `openPosition` | 91

##### Description
In the function [`openPosition`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L91 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") of the contract `FathomProxyWalletOwnerUpgradeable`, the transferred stablecoin amount equals the balance of the contract. This amount is not verified to match the parameter `_stablecoinAmount`. The function will not fail even if the factually transferred amount will be less than the requested `_stablecoinAmount` or even if no tokens will be transferred at all.
##### Recommendation
We recommend verifying that the transferred amount matches the requested amount.
##### Update
###### Client's response
We would like to exclude `FathomProxyWalletOwner` and  `FathomProxyWalletOwnerUpgradeable` from the audit scope.
