---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-03-27-blueberry-staking-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-03-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-03-27-Blueberry-Staking.md
tags:
- firm:0x52
- report:2024-03-27-blueberry-staking
title: '[M-01] \_fetchTWAP incorrectly assumes that blb is always token0 leading to
  bad pricing if it isn''t'
vuln_class: []
---

# [M-01] \_fetchTWAP incorrectly assumes that blb is always token0 leading to bad pricing if it isn't

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-03-27-Blueberry-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-03-27-Blueberry-Staking.md)_

---

**Details**

[BlueberryStaking.sol#L812-L819](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L812-L819)

    (int56[] memory tickCumulatives, ) = _pool.observe(_secondsArray);

    int56 _tickDifference = tickCumulatives[1] - tickCumulatives[0];
    int56 _timeDifference = int32(_observationPeriod);

    int24 _twapTick = int24(_tickDifference / _timeDifference);

    uint160 _sqrtPriceX96 = TickMath.getSqrtRatioAtTick(_twapTick);

We see above that the Uniswap V3 oracle price is always used directly as returned. Uniswap V3 always returns the price as a ratio of token0/token1. This means token0 is the base token and token1 is the quote token. Additionally Uniswap V3 sorts tokens by address meaning that blb can be either token0 or token1 depending on the stable asset.

In the event that blb is not token0, the price returned will be the inverse of the actual price since expected quote and base tokens are reversed. This will lead to largely incorrect prices that will either damage the user by grossly overcharging them or damage the treasury as vesting will be much cheaper than intended.

**Lines of Code**

[BlueberryStaking.sol#L798-L844](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L798-L844)

**Recommendation**

When adding the pool, check the pair order and store it. When querying the pool, reference back to this variable to determine if the price should be inverted.

**Remediation**

Fixed in [PR#30](https://github.com/Blueberryfi/blueberry-staking/pull/30/). Token order is now cached when setting Uniswap V3 pool. Price calculations have been adjusted to work regardless of token order.
