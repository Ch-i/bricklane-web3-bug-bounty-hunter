---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[ACKNOWLEDGED] Configuration addresses are not updatable in `FathomProxyWalletOwner`'
vuln_class: []
---

# [ACKNOWLEDGED] Configuration addresses are not updatable in `FathomProxyWalletOwner`

_Section severity (from Solodit section header): High_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwner.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L63 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") | contract `FathomProxyWalletOwner` >  `constructor` | 63

##### Description
In the `constructor` of the contract `FathomProxyWalletOwner`, several `address` type variables, such as `bookKeeper`, `positionManager`, `collateralTokenAdapter`, `stablecoinAdapter`, and so on, are initialized. These variables represent the contracts of the core structure of the protocol. If some of the addresses will get updated within the contracts of the core system, the wallet will not be able to interact with the updated contracts, such as in the case of the call to [`setCollateralPoolConfig`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/blob/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/BookKeeper.sol#L164) in the `BookKeeper` contract. The owner of the wallet won't be able to update already initialized addresses, which may result in a lock of the funds in the protocol.
##### Recommendation
We recommend adjusting the architecture for changing main contracts of the protocols by implementing a configuration contract with all recent addresses of the protocol and adding a migration mechanism.
##### Update
###### Client's response
We would like to exclude `FathomProxyWalletOwner` from the audit scope.
