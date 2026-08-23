---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Disable initializers in upgradable contracts'
vuln_class: []
---

# [FIXED] Disable initializers in upgradable contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwnerUpgradeable.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L17 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") | contract `FathomProxyWalletOwnerUpgradeable` | 17
[ProxyWalletRegistry.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/proxy-wallet/ProxyWalletRegistry.sol#L39 "/contracts/main/proxy-wallet/ProxyWalletRegistry.sol" "/contracts/main/proxy-wallet/ProxyWalletRegistry.sol") | contract `ProxyWalletRegistry` | 39

##### Description
The contract `FathomProxyWalletOwnerUpgradeable` and the contract `ProxyWalletRegistry` are upgradable, inheriting from the `Initializable` contract. However, the current implementation is missing the `_disableInitializers` function call in the constructor. Thus, an attacker can initialize the implementation. Usually, the initialized implementation has no direct impact on the proxy itself; however, it can be exploited in a phishing attack. In rare cases, the implementation might be mutable and may have an impact on the proxy.
Same applies to other upgradable contracts in the protocol.
##### Recommendation
We recommend calling `_disableInitializers` within the contract’s constructor to prevent the implementation from being initialized.
##### Update
###### Client's response
Fixed in commit [`657749cc9c6669c0c388588564e4dea946feed35`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/657749cc9c6669c0c388588564e4dea946feed35).
Fixed as suggested. added
```solidity
constructor() {
    _disableInitializers();
}
```

To upgradeable contracts so that `_disableInitializers` will be called at the moment of implementation deployment. Thanks for the advice.
