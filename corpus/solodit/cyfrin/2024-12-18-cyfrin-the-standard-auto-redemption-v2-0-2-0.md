---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Concentrated liquidity tick logic is incorrect
vuln_class: []
---

# Concentrated liquidity tick logic is incorrect

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** `AutoRedemption::calculateUSDsToTargetPrice` performs the following concentrated liquidity tick calculations to determine the current tick range corresponding to a given price:

```solidity
int24 _spacing = pool.tickSpacing();
(uint160 _sqrtPriceX96, int24 _tick,,,,,) = pool.slot0();
int24 _upperTick = _tick / _spacing * _spacing;
int24 _lowerTick = _upperTick - _spacing;
```

However, due to the behavior of signed integers in Solidity rounding _up_ to zero rather than the next lowest integer, this logic is only correct for negative ticks and positive ticks that are an exact multiple of `_spacing`. Otherwise, if `tick` is a positive non-multiple of `_spacing`, the calculated `_upperTick` and `_lowerTick` will correspond to the range immediately below the true current range.

This error could cause the subsequent `while` loop to execute even if the current price is above the target price, or enter the incorrect conditional branch and consider net liquidity even when the current tick should be considered within range:

```solidity
while (TickMath.getSqrtRatioAtTick(_lowerTick) < TARGET_PRICE) {
    uint256 _amount0;
    if (_tick > _lowerTick && _tick < _upperTick) {
        (_amount0,) = LiquidityAmounts.getAmountsForLiquidity(
            _sqrtPriceX96,
            TickMath.getSqrtRatioAtTick(_lowerTick),
            TickMath.getSqrtRatioAtTick(_upperTick),
            _liquidity
        );
    } else {
        (, int128 _liquidityNet,,,,,,) = pool.ticks(_lowerTick);
        _liquidity += uint128(_liquidityNet);
        (_amount0,) = LiquidityAmounts.getAmountsForLiquidity(
            _sqrtPriceX96,
            TickMath.getSqrtRatioAtTick(_lowerTick),
            TickMath.getSqrtRatioAtTick(_upperTick),
            _liquidity
        );
    }
    _usdc += _amount0;
    _lowerTick += _spacing;
    _upperTick += _spacing;
}
```

Fortunately, this is highly unlikely to occur due to the difference in `USDs` and `USDC` decimals (`18` and `6` respectively). In calculation of `sqrtPriceX96`, which is a fixed point `Q64.96` number representing the square root of the ratio of the two pool assets (`token1`/`token0`), `USDs` is `token0` and `USDC` is `token1`. Given that the relative value of the two pool assets is expected to be reasonably stable, with the `TARGET_PRICE` defined as `79228162514264337593543` which corresponds to a ratio of `1e-12`, the square root price will realistically always be on the order $10^{-6}$:

$$\text{price ratio (token1/token0)} = \frac{10^{\text{USDC decimals}}}{10^{\text{USDs decimals}}} = \frac{10^{6}}{10^{18}} = 10^{-12}$$

$$\sqrt{\text{price ratio}} = \sqrt{10^{-12}} = 10^{-6}$$

This means the pool tick should realistically always be negative considering that a tick represents the logarithmic index of the price ratio, and the logarithm is negative since the ratio $10^{-12}$ is much smaller than 1:

$$\text{tick}=\log_{
\sqrt{(1.0001)}}(\text{price ratio})$$

It would take a de-peg event of unrealistic magnitude to cause this to be an issue, although `USDC` is upgradeable and so this caveat should not be relied upon.

**Impact:** The `USDs` calculation could be affected by errors in the calculation of tick ranges.

**Recommended Mitigation:** Modify the logic to consider the sign of `_tick` when calculating tick ranges.

**The Standard DAO:** Acknowledged. `AutoRedemption` will be deployed with trigger price of at negative tick, target price is at negative tick. Upkeep is only required between trigger price tick (or lower) and target price tick. Ticks are therefore not going to be positive.

**Cyfrin:** Acknowledged, based on the assumption that Circle does not update the decimals of `USDC`.
