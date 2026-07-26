---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-01-19-fathom-stablecoin-0-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md
tags:
- firm:oxorio
- report:2024-01-19-fathom-stablecoin
title: '[ACKNOWLEDGED] Missing overflow checks in `PluginPriceOracle`'
vuln_class: []
---

# [ACKNOWLEDGED] Missing overflow checks in `PluginPriceOracle`

_Section severity (from Solodit section header): High_  
_Audit firm: Oxorio_  
_Source report: [2024-01-19-Fathom Stablecoin.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom%20Stablecoin.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[PluginPriceOracle.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/price-oracles/PluginPriceOracle.sol#L43 "/contracts/main/price-oracles/PluginPriceOracle.sol" "/contracts/main/price-oracles/PluginPriceOracle.sol") | contract `PluginPriceOracle` > function `getPrice` | 43

##### Description
In the function `getPrice` of the contract `PluginPriceOracle`, there is a `latestAnswer` call to the `oracle` contract, which returns the `int256` variable. This `int256` variable is casted to the `uint256` type. Since the received variable from the `oracle` contract is of type `int256`, it can be negative, and by casting a negative variable into the `uint256` type, underflow occurs. As an example: when the oracle is returning `-1`, the result after the `uint256` type casting is `115792089237316195423570985008687907853269984665640564039457584007913129639935`, and after the conversion, the function will revert in the `_toWad` function call because this big underflowed variable with the multiplication to `10**14` will lead to overflow. The overflow with the multiplication will revert because with the Solidity version `0.8.0` and later, there is checked math which protects from having overflow and underflow issues with arithmetic. Despite the fact that revert will occur in the price oracle contract, the overall architecture of the Fathom protocol will handle this situation; however, it's possible that the `latestAnswer` call returns a big negative value, which after the casting and underflow will lead to a smaller `price` that won't revert during the `_toWad` call and later during the calculations. This will lead to the inflated price of the collateral in the system, inability to perform liquidations, and other unexpected behavior.
##### Recommendation
We recommend validating the return variable of the `latestAnswer` function call to be a positive value.
##### Update
###### Client's response
We would like to exclude `PluginPriceOracle` from the audit scope.
