---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[ACKNOWLEDGED] Gas consumption limitations for integrators in `FathomStablecoinProxyActions`'
vuln_class: []
---

# [ACKNOWLEDGED] Gas consumption limitations for integrators in `FathomStablecoinProxyActions`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FathomStablecoinProxyActions.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol#L143 "/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol" "/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol") | contract `FathomStablecoinProxyActions` > function `wipeAndUnlockXDC` | 143

##### Description
In the function [`wipeAndUnlockXDC`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol#L143 "/contracts/main/proxy-actions/FathomStablecoinProxyActions.sol") of the `FathomStablecoinProxyActions` contract, there is a gas consumption limitation in the `safeTransferETH` call. This limitation can result in a failed transaction if the integrator is using the `receive` function with custom and gas-heavy logic.
##### Recommendation
We recommend a thorough review of the existing logic.
##### Update
###### Client's response
Described concern is understandable. The intention of limiting the gas amount to 21,000 was to ensure that the gas is only sufficient for the `ETH` transfer and nothing more.
