---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-3-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] Using constant in `CurveStratBase`'
vuln_class: []
---

# [FIXED] Using constant in `CurveStratBase`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[CurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/CurveStratBase.sol#L36 "/contracts/strategies/curve/CurveStratBase.sol") | contract `CurveStratBase` > function `checkDepositSuccessful` | 36
[ERC4626StratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/erc4626/ERC4626StratBase.sol#L40 "/contracts/strategies/erc4626/ERC4626StratBase.sol") | contract `ERC4626StratBase` > function `checkDepositSuccessful` | 40

##### Description
In this locations, a hardcoded number `5` is used:
```solidity
    for (uint256 i = 0; i < 5; i++) {
```
##### Recommendation
We recommend using the `POOL_ASSETS` constant instead of a hardcoded number.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).
