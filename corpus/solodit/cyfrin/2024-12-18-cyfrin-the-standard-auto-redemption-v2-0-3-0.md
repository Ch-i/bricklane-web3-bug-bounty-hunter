---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: '`AutoRedemption::calculateUSDsToTargetPrice` could be refactored to avoid
  repeated logic'
vuln_class: []
---

# `AutoRedemption::calculateUSDsToTargetPrice` could be refactored to avoid repeated logic

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** When calculating the target `USDs` amount, the call to `LiquidityAmounts::getAmountsForLiquidity` is common to both conditional branches, with the liquidity parameter being the only difference:

```solidity
uint128 _liquidity = pool.liquidity();
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
    ...
}
```

This could be refactored to avoid repeated code such that it is only the liquidity calculations that remain in the conditionals.

**The Standard DAO:** Fixed by commit [e48ccff](https://github.com/the-standard/smart-vault/commit/e48ccff9f33be2871cfce47312451e03a359f6cc).

**Cyfrin:** Verified. The logic has been correctly refactored to only consider the net liquidity delta when the current tick is below the range.
