---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[ACKNOWLEDGED] Use of outdated libraries'
vuln_class: []
---

# [ACKNOWLEDGED] Use of outdated libraries

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FixedSpreadLiquidationStrategy.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol#L202 "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol" "/contracts/main/stablecoin-core/liquidation-strategies/FixedSpreadLiquidationStrategy.sol") | contract `FixedSpreadLiquidationStrategy` > function `execute` | 202

##### Description
The protocol currently employs the following versions of the OpenZeppelin libraries:
```json
"@openzeppelin/contracts": "4.4.1",
"@openzeppelin/contracts-upgradeable": "4.4.1",
```
These versions are considered outdated, with the current version of the OpenZeppelin library being `v5.0.1`. The use of outdated libraries increases the risk of vulnerabilities in the code. According to [SNYK](https://security.snyk.io/package/npm/@openzeppelin%2Fcontracts/4.4.1), the current version of the library (v5.0.1) addresses multiple High and Medium issues. For instance, in the `execute` function of the `FixedSpreadLiquidationStrategy` contract, there is a `supportsInterface` call that can consume excessive resources when processing a large amount of data via an EIP-165 and revert, potentially leading to a Denial of Service (DoS) attack. While this issue doesn't directly impact the `FixedSpreadLiquidationStrategy` itself, the `_collateralRecipient` could be affected. Consequently, it is strongly recommended to update the OpenZeppelin package.
##### Recommendation
We recommend updating the OpenZeppelin package to the latest version (v5.0.1).
##### Update
###### Client's response
The concern raised is acknowledged and understood. While upgrading to the recommended version 5.0.1 of OpenZeppelin (OZ) would be ideal, such an upgrade from our current version 4.4.1 to 5.0.1 necessitates substantial changes to the codebase. Therefore, at this stage, we have opted to update the OZ version from 4.4.1 to 4.9.2. This interim upgrade has been implemented in commit `fa337f9778480a55d4c24274b9c315a55952e308`.
