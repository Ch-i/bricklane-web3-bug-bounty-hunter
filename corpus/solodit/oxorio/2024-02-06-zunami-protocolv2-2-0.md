---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[ACKNOWLEDGED] High slippage in `CrvUsdApsConvexCurveStratBase`, `FraxApsConvexCurveStratBase`'
vuln_class: []
---

# [ACKNOWLEDGED] High slippage in `CrvUsdApsConvexCurveStratBase`, `FraxApsConvexCurveStratBase`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[CrvUsdApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol#L90 "/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol") | contract `CrvUsdApsConvexCurveStratBase` > function `inflate` | 90
[CrvUsdApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol#L125 "/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol") | contract `CrvUsdApsConvexCurveStratBase` > function `deflate` | 125
[FraxApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol#L91 "/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol") | contract `FraxApsConvexCurveStratBase` > function `inflate` | 91
[FraxApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol#L121 "/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol") | contract `FraxApsConvexCurveStratBase` > function `deflate` | 121

##### Description
The functions `inflate` and `deflate` in the contracts `CrvUsdApsConvexCurveStratBase` and `FraxApsConvexCurveStratBase` use the `minDeflateAmount` parameter, which limits slippage and is valued in USD, set in advance as a function parameter. This could lead to transaction reversion if the limit is too low or result in high slippage.

##### Recommendation
We recommend refactoring the slippage limitation mechanism of the APS strategies.

##### Update

###### Oxorio's response
We recommend implementing a percent-based slippage mechanism instead of a fixed value slippage in USD, to ensure that the slippage logic does not depend on fluctuations in the price of the asset used.

For example:
The `zunUSD` price is `0.9` USD, and it is necessary to exchange 10,000 `zunUSD` for `crvUsd` using the `deflate` method to equalize the exchange rate. Setting the slippage:
- In the current implementation: 90 USD (= 1%)
- In a percent-based implementation: 1% (= 90 USD)

Let's say the `zunUSD` price is `0.7` USD at the moment of transaction execution. So, the acceptable slippage is:
- In the current implementation: 90 USD (= 1.3%)
- In a percent-based implementation: 1% (= 70 USD)

As a result, the acceptable slippage in the current implementation is `1.3%`, which is more than the initial `1%`.

###### Zunami's response
In the `deflate` and `inflate` methods, two parameters are used: a percentage of the managed capital strategy in the external protocol and a minimum number of tokens. In the case of inflation, the second parameter determines the minimum number of stables that were obtained when withdrawing the tokens from the external pool and depositting the `Zunami Pool` to mint `zun` stables and return them back to the external protocol, thereby expanding the emission of zun stables. In the case of deflation, it determines the minimum number of stables that were obtained when converting `zun` stables before being deposited into the external protocol. Since the first parameter is initially specified in percentages, the minimum expected number of tokens after all conversions is specified in units, not percentages, to minimize the attack vector at the time of withdrawal and conversion. Therefore, specifying the second parameter as a percentage of slippage is considered a riskier scenario than specifying an explicit minimum number of tokens withdrawn.
