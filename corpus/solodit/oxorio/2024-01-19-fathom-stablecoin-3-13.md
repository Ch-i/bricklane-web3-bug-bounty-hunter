---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-13
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
title: '[ACKNOWLEDGED] Typo in `FathomProxyWalletOwner`'
vuln_class: []
---

# [ACKNOWLEDGED] Typo in `FathomProxyWalletOwner`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwner.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L207 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") | contract `FathomProxyWalletOwner` | 207

##### Description
In the contract `FathomProxyWalletOwner`, there is a typo in the function name `_successfullXDCTransfer` instead of `_successfulXDCTransfer`.
##### Recommendation
We recommend correcting the typo to `_successfulXDCTransfer` for consistency and clarity.
##### Update
###### Client's response
We would like to exclude `FathomProxyWalletOwner` and `FathomProxyWalletOwnerUpgradeable`  from the audit scope.
