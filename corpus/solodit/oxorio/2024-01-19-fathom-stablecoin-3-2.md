---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Unsafe usage of `abi.encodeWithSelector` in `SafeToken`'
vuln_class: []
---

# [FIXED] Unsafe usage of `abi.encodeWithSelector` in `SafeToken`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[SafeToken.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/utils/SafeToken.sol#L27 "/contracts/main/utils/SafeToken.sol" "/contracts/main/utils/SafeToken.sol") | contract `SafeToken` > function `safeTransfer` | 27

##### Description
In the function [`safeTransfer`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/utils/SafeToken.sol#L27 "/contracts/main/utils/SafeToken.sol") of the `SafeToken` contract, `abi.encodeWithSelector` is used instead of `abi.encodeCall`. Since version `0.8.11`, `abi.encodeCall` provides a type-safe encoding utility compared to `abi.encodeWithSelector`. While `abi.encodeWithSelector` can be used with `interface.<function>.selector` to prevent typographical errors, it lacks type checking during compile time, a feature offered by `abi.encodeCall`.
##### Recommendation
We recommend using `abi.encodeCall` instead of `abi.encodeWithSelector` to adhere to [best practices](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3693) in the web3 sphere.
##### Update
###### Client's response
Fixed in commit [`327df2174f5c9514b3dc2c692adde3e5a293432e`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/327df2174f5c9514b3dc2c692adde3e5a293432e).
Fixed as suggested.
