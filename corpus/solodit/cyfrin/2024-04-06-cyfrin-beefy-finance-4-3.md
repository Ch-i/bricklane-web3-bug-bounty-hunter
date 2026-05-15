---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Optimize `StrategyPassiveManagerUniswap::_chargeFees` to remove unnecessary
  variables and eliminate duplicate storage reads
vuln_class: []
---

# Optimize `StrategyPassiveManagerUniswap::_chargeFees` to remove unnecessary variables and eliminate duplicate storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StrategyPassiveManagerUniswap::_chargeFees` uses two unnecessary variables `out0` and `out1` and reads the same storage values from `lpToken0`, `lpToken` and `native` multiple times. A more optimized version of the relevant section looks like this:

```solidity
// @audit cache `native` to prevent duplicate storage reads
address nativeCached = native;

/// We calculate how much to swap and then swap both tokens to native and charge fees.
uint256 nativeEarned;
if (_amount0 > 0) {
    // Calculate amount of token 0 to swap for fees.
    uint256 amountToSwap0 = _amount0 * fees.total / DIVISOR;
    _amountLeft0 = _amount0 - amountToSwap0;

    // @audit next section refactored
    // If token0 is not native, swap to native the fee amount.
    if (lpToken0 != nativeCached) nativeEarned += UniV3Utils.swap(unirouter, lpToken0ToNativePath, amountToSwap0);

    // Add the native earned to the total of native we earned for beefy fees, handle if token0 is native.
    else nativeEarned += amountToSwap0;
}

if (_amount1 > 0) {
    // Calculate amount of token 1 to swap for fees.
    uint256 amountToSwap1 = _amount1 * fees.total / DIVISOR;
    _amountLeft1 = _amount1 - amountToSwap1;

    // @audit next section refactored
    // Add the native earned to the total of native we earned for beefy fees, handle if token1 is native.
    if (lpToken1 != nativeCached) nativeEarned += UniV3Utils.swap(unirouter, lpToken1ToNativePath, amountToSwap1);

    // Add the native earned to the total of native we earned for beefy fees, handle if token1 is native.
    else nativeEarned += amountToSwap1;
}

// @audit then use `nativeCached` in the transfers eg:
IERC20Metadata(nativeCached).safeTransfer(_callFeeRecipient, callFeeAmount);
```

**Beefy:**
Acknowledged.
