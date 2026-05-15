---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-0
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
title: '[ACKNOWLEDGED] Addresses are not validated in `FathomProxyWalletOwner`'
vuln_class: []
---

# [ACKNOWLEDGED] Addresses are not validated in `FathomProxyWalletOwner`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwner.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L47 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") | contract `FathomProxyWalletOwner` >  `constructor` | 47

##### Description
In the `constructor` of the contract `FathomProxyWalletOwner`, the addresses of the protocol contracts are supplied by the user. While the addresses get validated for being empty, no validation is performed that those addresses represent correct entities of the protocol or represent contracts at all. The interfaces are not ensured for supplied addresses.
##### Recommendation
We recommend deploying `FathomProxyWalletOwner` as a clone or using a factory contract, or validating addresses to represent legitimate instances of the protocol. The protocol can benefit from the architecture with a centralized configuration contract. Using ERC165 to validate interface implementation is advised.
##### Update
###### Client's response
We would like to exclude  `FathomProxyWalletOwner` from the audit scope.
