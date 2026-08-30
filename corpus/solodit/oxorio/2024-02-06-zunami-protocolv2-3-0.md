---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] Inflation attack in `ZunamiPool`'
vuln_class: []
---

# [FIXED] Inflation attack in `ZunamiPool`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[ZunamiPool.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/ZunamiPool.sol#L196 "/contracts/ZunamiPool.sol") | contract `ZunamiPool` > function `processSuccessfulDeposit` | 196

##### Description
In the function `processSuccessfulDeposit` of the `ZunamiPool` contract, the balance of the contract can be inflated by directly sending funds. This can result in an incorrect amount of shares issued.
```solidity
  minted =
    ((totalSupply() + 10 ** _decimalsOffset()) * depositedValue) /
    (totalDeposited + 1);
```
The attacker can front-run the first deposit and inflate the `totalDeposited` variable, resulting in zero shares being minted. While this attack results in loss for the attacker, the user still can loose their deposit.

##### Recommendation
We recommend increasing the `_decimalsOffset` value (for example `3`).

##### Update
Fixed in commit [`79892fe12bec407d3d9706c19cd421d458263c0c`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/79892fe12bec407d3d9706c19cd421d458263c0c/).
