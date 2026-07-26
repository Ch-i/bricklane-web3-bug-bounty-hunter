---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[ACKNOWLEDGED] Possibility of misconfiguration in `FathomProxyWalletOwner`'
vuln_class: []
---

# [ACKNOWLEDGED] Possibility of misconfiguration in `FathomProxyWalletOwner`

_Section severity (from Solodit section header): High_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwner.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L56 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") | contract `FathomProxyWalletOwner` >  `constructor` | 56

##### Description
In the `constructor` of the contract `FathomProxyWalletOwner`, several `address` type variables, such as `bookKeeper`, `positionManager`, `collateralTokenAdapter`, `stablecoinAdapter`, and so on, are initialized. These variables represent the contracts of the core structure of the protocol. While these contracts are assumed to work as a completely synchronized set, nothing prevents a user from initializing a wallet with the addresses of the contracts that are not synced with each other, like using an address of some obsolete version of one of the contracts. 
In such a case, the wallet contract may work incorrectly, possibly resulting in a lock of funds.
##### Recommendation
We recommend having a factory or clones contract for the deployment of the `FathomProxyWalletOwner` contract or utilizing an external call to the Configuration contract with all addresses.
##### Update
###### Client's response
Thanks for the finding. We would like to exclude `FathomProxyWalletOwner ` from the audit scope.
