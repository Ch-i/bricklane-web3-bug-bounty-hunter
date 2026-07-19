---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: '`USDs` redemption calculation can be manipulated due to unsafe signed-unsigned
  cast'
vuln_class: []
---

# `USDs` redemption calculation can be manipulated due to unsafe signed-unsigned cast

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** The following logic is executed when calculating the `USDs` redemption amount, after the tick range has been advanced beyond that of the current tick:

```solidity
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
```

The `_liquidityNet` variable represents the net active liquidity delta when crossing between tick ranges, so this is considered along with the active liquidity of the original range; however, this value is cast from a signed integer to unsigned without actually checking the sign. Given that negative signed integers are represented using two's complement, net negative liquidities (i.e. less active liquidity in the subsequent range) will silently result in the incremented `_liquidity` being a very large number. This scenario could occur accidentally, or be forced by an attacker by the addition of just-in-time (JIT) liquidity, causing the target vault to be fully redeemed for the maximum `USDs`:

```solidity
if (_USDsTargetAmount > _vaultData.status.minted) _USDsTargetAmount = _vaultData.status.minted;
```

**Impact:** In the best case, more debt could be repaid than intended. In the worst case, fulfilment could be made to revert which will permanently disable auto redemption functionality (as described in a separate issue).

**Recommended Mitigation:** The sign of `_liquidityNet` should be checked before incrementing `_liquidity`, subtracting the absolute value if it is negative. Consider using the `LiquidityMath` [library](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/LiquidityMath.sol).

**The Standard DAO:** Fixed by commit [49af007](https://github.com/the-standard/smart-vault/commit/49af007bcce5079ebfdc3de8f0c231ec4d0f121c).

**Cyfrin:** Verified. The `LiquidityMath` library is now used.
