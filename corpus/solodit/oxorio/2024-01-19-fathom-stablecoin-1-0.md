---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[ACKNOWLEDGED] Owner fails to receive native token transfer in `FathomProxyWalletOwner`'
vuln_class: []
---

# [ACKNOWLEDGED] Owner fails to receive native token transfer in `FathomProxyWalletOwner`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwner.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L139 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") | contract `FathomProxyWalletOwner` > function `closePositionFull` | 139
[FathomProxyWalletOwner.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L154 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") | contract `FathomProxyWalletOwner` > function `withdrawXDC` | 154

##### Description
In the function [`closePositionFull`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L139 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") and the function [`withdrawXDC`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L154 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol"), the token transfer is performed through the `call` operation to the `msg.sender` cast to `payable` type. The modifier `onlyOwner` ensures that `msg.sender` is the owner of the contract.
The assumption that the owner is always able to receive the transfer may be broken, as in the case when ownership is transferred to the contract without the `receive` method. This will result in the inability to close the position or withdraw native tokens from the protocol.
##### Recommendation
We recommend implementing the ERC165 interface to ensure that the owner of the contract is able to receive native tokens.
##### Update
###### Client's response
We would like to exclude `PluginPriceOracle ` from the audit scope.
