---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[NO ISSUE] Add migration mechanism in `CollateralPoolConfig`'
vuln_class: []
---

# [NO ISSUE] Add migration mechanism in `CollateralPoolConfig`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[CollateralPoolConfig.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol#L173 "/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol" "/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol") | contract `CollateralPoolConfig` | 173

##### Description
The function [`setAdapter`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol#L173 "/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol") in the contract `CollateralPoolConfig` updates the adapter reference in the contract. At the same time, other contracts are not upgraded with this change, which will lead to the usage of different contracts in the protocol and result in unexpected behavior. For example, with the update of the `adapter` in the `CollateralPoolConfig` contract, the `adapter` is not updated in the `FlashMintModule` contract.
##### Recommendation
We recommend adding a migration mechanism that accounts for all side effects of updating contracts.
##### Update
###### Client's response
Fix No Need

Major 3 is about, what happens to `FlashMintModule` if `collateralTokenAdapter` address changes via `CollateralPoolConfig`,  But `FlashMintModule` doesn't use `collateralTokenAdapter` but only uses `stablecoinAdapter`. 
There are also two more address setter fns in the `CollateralPoolConfig` contract. They are `setPriceFeed` fn and `setStrategy` fn. Contract that uses `priceFeedAddress` of a specific `collateralPool` does not save the `priceFeedAddress` in storage but fetches `priceFeedAddress` from `CollateralPoolConfig` contract. Therefore, `setPriceFeed` in `collateralPoolConfig` does not affect other contracts as was concerned in the issue.
Same for `setStrategy`.
