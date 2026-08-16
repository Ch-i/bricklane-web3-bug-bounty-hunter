---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-12
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] Missing `require` check in `FlashMintModule`'
vuln_class: []
---

# [FIXED] Missing `require` check in `FlashMintModule`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FlashMintModule.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/flash-mint/FlashMintModule.sol#L162 "/contracts/main/flash-mint/FlashMintModule.sol" "/contracts/main/flash-mint/FlashMintModule.sol") | contract `FlashMintModule` > function `flashLoan` | 162

##### Description
In the function `flashLoan` of the contract `FlashMintModule`, there is no validation that after the `settleSystemBadDebt` call, the current amount of the `stablecoin` in `BookKeeper` equals or is greater than the previous amount plus fees, while this check is present in the `bookKeeperFlashLoan` function.
##### Recommendation
We recommend adding the same `require` to the `flashLoan` function to ensure the same level of security in both functions.
##### Update
###### Client's response
Fixed in commit [`754fd35abc2c6ea77e5e4e375fb587b8fcf114a6`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/754fd35abc2c6ea77e5e4e375fb587b8fcf114a6).
Fixed as suggested.
