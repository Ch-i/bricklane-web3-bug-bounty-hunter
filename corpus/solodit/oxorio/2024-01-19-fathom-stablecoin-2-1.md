---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[ACKNOWLEDGED] DDOS attack in `FathomProxyWalletOwnerUpgradeable`'
vuln_class: []
---

# [ACKNOWLEDGED] DDOS attack in `FathomProxyWalletOwnerUpgradeable`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwnerUpgradeable.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L37 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") | contract `FathomProxyWalletOwnerUpgradeable` > function `receive` | 37

##### Description
In the function [`receive`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L37 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") of the contract `FathomProxyWalletOwnerUpgradeable`, the event is emitted notifying about received funds. The entities subscribed to this event may experience denial of service in case a malicious actor would spam the contract with transfers of negligible amounts (1 wei) of native tokens. This can cause unexpected behavior for integrators using the `FathomProxyWalletOwnerUpgradeable` contract.
##### Recommendation
We recommend removing the `emit` or notifying all external integrators not to use this event for production monitoring; this `emit` should be used only for checking historical values.
##### Update
###### Client's response
We would like to exclude `FathomProxyWalletOwner` and  `FathomProxyWalletOwnerUpgradeable` from the audit scope.
