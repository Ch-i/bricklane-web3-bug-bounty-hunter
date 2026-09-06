---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[FIXED] `feeRate` is not limited in `FlashMintModule`'
vuln_class: []
---

# [FIXED] `feeRate` is not limited in `FlashMintModule`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FlashMintModule.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/flash-mint/FlashMintModule.sol#L122 "/contracts/main/flash-mint/FlashMintModule.sol" "/contracts/main/flash-mint/FlashMintModule.sol") | contract `FlashMintModule` > function `setFeeRate` | 122

##### Description
In the function [`setFeeRate`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/flash-mint/FlashMintModule.sol#L122 "/contracts/main/flash-mint/FlashMintModule.sol") of the contract `FlashMintModule`, the `feeRate` is unbounded when it's getting set. The `feeRate` variable can be set greater than `WAD`, which will lead to the accumulation of fees greater than the actual flash loan amount.
##### Recommendation
We recommend validating the `feeRate` value.
##### Update
###### Client's response
Fixed in commit [`a23bebf1b097aec1754ed692f87b8d31e239ec2f`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/a23bebf1b097aec1754ed692f87b8d31e239ec2f).
Fixed as suggested. 

set limitation to `feeRate`. The `feeRate` cannot be higher than `WAD` since `WAD` is 100%.
