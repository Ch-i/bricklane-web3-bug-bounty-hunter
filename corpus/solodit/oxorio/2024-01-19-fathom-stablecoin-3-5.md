---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-5
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
title: '[ACKNOWLEDGED] Check is not performed prior to sending funds in `FathomProxyWalletOwner`'
vuln_class: []
---

# [ACKNOWLEDGED] Check is not performed prior to sending funds in `FathomProxyWalletOwner`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwner.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L114 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") | contract `FathomProxyWalletOwner` > function `closePositionPartial` | 114

##### Description
In the function [`closePositionPartial`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L114) of the contract `FathomProxyWalletOwner`, the `wipeAndUnlockXDC` call sends native tokens to the `FathomProxyWalletOwner` only when `_collateralAmount > 0`. However, the following call:
```solidity
(bool sent, ) = payable(msg.sender).call{ value: address(this).balance }("");
```
which sends the whole balance of the contract, is always executed.
Same applies to the upgradeable version of the contract.
##### Recommendation
We recommend executing the transfer of the balance only if funds were received after the `wipeAndUnlockXDC` function call.
##### Update
###### Client's response
We would like to exclude `FathomProxyWalletOwner` and `FathomProxyWalletOwnerUpgradeable`  from the audit scope.
