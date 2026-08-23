---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] Parameter validation'
vuln_class: []
---

# [FIXED] Parameter validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[FraxApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol#L46-L47 "/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol") | contract `FraxApsConvexCurveStratBase` >  `constructor` | 46-47
[CrvUsdApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol#L45-L46 "/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol") | contract `CrvUsdApsConvexCurveStratBase` >  `constructor` | 45-46
[ConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/ConvexCurveStratBase.sol#L22-L23 "/contracts/strategies/curve/convex/ConvexCurveStratBase.sol") | contract `ConvexCurveStratBase` >  `constructor` | 22-23
[CurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/CurveStratBase.sol#L19-L20 "/contracts/strategies/curve/CurveStratBase.sol") | contract `CurveStratBase` >  `constructor` | 19-20
[StakeDaoCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/stakeDao/StakeDaoCurveStratBase.sol#L15 "/contracts/strategies/curve/stakeDao/StakeDaoCurveStratBase.sol") | contract `StakeDaoCurveStratBase` >  `constructor` | 15
[RecapitalizationManager.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/staking/RecapitalizationManager.sol#L31 "/contracts/staking/RecapitalizationManager.sol") | contract `RecapitalizationManager` > `constructor` | 31
[StakingRewardDistributor.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/staking/StakingRewardDistributor.sol#L430 "/contracts/staking/StakingRewardDistributor.sol") | contract `StakingRewardDistributor` > function `withdrawEmergency` | 430
[StakingRewardDistributor.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/staking/StakingRewardDistributor.sol#L381 "/contracts/staking/StakingRewardDistributor.sol") | contract `StakingRewardDistributor` > function `claim` | 381
[StakingRewardDistributor.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/staking/StakingRewardDistributor.sol#L300 "/contracts/staking/StakingRewardDistributor.sol") | contract `StakingRewardDistributor` > function `updatePool` | 300
[StakingRewardDistributor.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/blob/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/staking/StakingRewardDistributor.sol#L471 "/contracts/staking/StakingRewardDistributor.sol") | contract `StakingRewardDistributor` > function `reallocatePool` | 471
[StakingRewardDistributor.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/blob/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/staking/StakingRewardDistributor.sol#L152 "/contracts/staking/StakingRewardDistributor.sol") | contract `StakingRewardDistributor` > function `addPool` | 152
[StakingRewardDistributor.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/blob/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/staking/StakingRewardDistributor.sol#L131 "/contracts/staking/StakingRewardDistributor.sol") | contract `StakingRewardDistributor` > function `addRewardToken` | 131
[ZunDistributor.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/blob/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/distributor/ZunDistributor.sol#L78" "/contracts/distributor/ZunDistributor.sol") | contract `ZunDistributor` > function `constructor` | 78
[GenericOracle.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/lib/ConicOracle/contracts/oracles/GenericOracle.sol#L43 "/contracts/lib/ConicOracle/contracts/oracles/GenericOracle.sol") | contract `GenericOracle` > function `setCustomOracle` | 43
[ZunamiStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/ZunamiStratBase.sol#L32 "/contracts/strategies/ZunamiStratBase.sol") | contract `ZunamiStratBase` > `constructor` | 32
[ZunamiStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/ZunamiStratBase.sol#L33 "/contracts/strategies/ZunamiStratBase.sol") | contract `ZunamiStratBase` > `constructor` | 33

##### Description
In the locations mentioned above, function parameters are not validated. This lack of validation can lead to unpredictable behavior or the occurrence of panic errors.
##### Recommendation
We recommend implementing validation for function parameters to ensure stable and predictable behavior.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).
