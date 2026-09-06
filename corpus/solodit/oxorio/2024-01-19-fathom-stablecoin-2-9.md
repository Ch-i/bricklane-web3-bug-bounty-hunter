---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-2-9
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
title: '[ACKNOWLEDGED] Lack of sanity check in `CollateralPoolConfig`'
vuln_class: []
---

# [ACKNOWLEDGED] Lack of sanity check in `CollateralPoolConfig`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[CollateralPoolConfig.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol#L212 "/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol" "/contracts/main/stablecoin-core/config/CollateralPoolConfig.sol") | contract `CollateralPoolConfig` > function `setStrategy` | 212

##### Description
In the `setStrategy` function of the `CollateralPoolConfig` contract, there is no sanity check call to validate if the provided `strategy` has the correct interface. An incorrect `strategy` address will lead to failed liquidation transactions.
##### Recommendation
We recommend verifying the `strategy` address by incorporating a sanity check call to the `flashLendingEnabled` variable.
##### Update
###### Client's response
The described concern is understandable. However, there is not much utility, at the moment, in making the change since checking whether `flashLendingEnabled` return bool or not doesn’t necessarily check if the new `fixedSpreadLiquidationStrategy` is really valid or not.
