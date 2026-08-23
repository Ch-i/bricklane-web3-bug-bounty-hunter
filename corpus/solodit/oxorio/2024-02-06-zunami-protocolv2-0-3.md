---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-0-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] Price-feed returns ETH price in `FrxETHOracle`'
vuln_class: []
---

# [FIXED] Price-feed returns ETH price in `FrxETHOracle`

_Section severity (from Solodit section header): High_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FrxETHOracle.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/lib/ConicOracle/contracts/oracles/FrxETHOracle.sol#L27 "/contracts/lib/ConicOracle/contracts/oracles/FrxETHOracle.sol") | contract `FrxETHOracle` | 27

##### Description
In the contract `FrxETHOracle` the oracle requests the price for `ETH` instead of the price of `frxETH`. `frxETH` peg is defined as 1% on each side of `1.00` exchange rate meaning the `frxETH` exchange rate rests between `1.01-0.99` `ETH` per 1 `frxETH`. In case of depeg, oracle will return incorrect value.
##### Recommendation
We recommend changing the code to return the correct price of `frxETH`.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).
