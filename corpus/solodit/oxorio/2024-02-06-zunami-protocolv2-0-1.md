---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] Blocking execution of `inflate` and `deflate` functions in `ConvexCurveStratBase`'
vuln_class: []
---

# [FIXED] Blocking execution of `inflate` and `deflate` functions in `ConvexCurveStratBase`

_Section severity (from Solodit section header): High_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[ConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/ConvexCurveStratBase.sol#L32 "/contracts/strategies/curve/convex/ConvexCurveStratBase.sol") | contract `ConvexCurveStratBase` > function `depositBooster` | 32

##### Description
In the `depositBooster` function of the `ConvexCurveStratBase` contract, the `allowance` is increased by an amount that may be insufficient for the subsequent call to `depositAll`. This issue arises during the call to [`depositAll`](https://github.com/convex-eth/platform/blob/main/contracts/contracts/Booster.sol#L289) in Convex, where a deposit is made for the entire balance of the strategy:
```solidity
uint256 balance = IERC20(lptoken).balanceOf(msg.sender);
deposit(_pid, balance, _stake);
```
This leads to a problem where, if there are LP tokens on the strategy contract, calling the `inflate` and `deflate` functions can result in an error due to insufficient `allowance` in the `depositBooster` function.
Additionally, it is possible to frontrun transactions calling the `inflate` and `deflate` functions, blocking their execution by adding a small amount of LP tokens to the strategy contract.

##### Recommendation
We recommend considering the replacement of the `depositAll` function call with a call to the `deposit` function, explicitly specifying the `amount`.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).
