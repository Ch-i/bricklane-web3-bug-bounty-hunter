---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-5-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Unnecessary native token checks
vuln_class: []
---

# Unnecessary native token checks

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** `FullRangeHook::beforeInitialize` attempts to retrieve the symbol of both currencies, with explicit handling of the native token; however, it is not possible for `currency1` to be the native token given ordering rules in Uniswap (`currency0` < `currency1`) since it is represented as `address(0)`.

```solidity
// Prepare the symbol for the LP token to be deployed
string memory symbol0 =
    key.currency0.isAddressZero() ? NATIVE_CURRENCY_SYMBOL : IERC20Metadata(Currency.unwrap(key.currency0)).symbol();
string memory symbol1 =
    key.currency1.isAddressZero() ? NATIVE_CURRENCY_SYMBOL : IERC20Metadata(Currency.unwrap(key.currency1)).symbol();
```

The same happens when returning the native value sent to the contract during delta settlement. It currently checks both tokens to be the zero address but in reality only token 0 can be the native token.

```solidity
    /// @dev Settles any deltas after adding/removing liquidity
    function _settleDeltas(address sender, PoolKey memory key, BalanceDelta delta) internal {
        key.currency0.settle(poolManager, sender, uint256(int256(-delta.amount0())), false);
        key.currency1.settle(poolManager, sender, uint256(int256(-delta.amount1())), false);
@>      if (key.currency0.isAddressZero() || key.currency1.isAddressZero()) _returnNative(sender);
    }
```

**Recommended Mitigation:** The second ternary operator can be removed since it is guaranteed that `currency1` will not be the native token.

```diff
   string memory symbol0 =
       key.currency0.isAddressZero() ? NATIVE_CURRENCY_SYMBOL : IERC20Metadata(Currency.unwrap(key.currency0)).symbol();
-- string memory symbol1 =
--     key.currency1.isAddressZero() ? NATIVE_CURRENCY_SYMBOL : IERC20Metadata(Currency.unwrap(key.currency1)).symbol();
++ string memory symbol1 = IERC20Metadata(Currency.unwrap(key.currency1)).symbol();
```

For returning the native value, it is only necessary to check for token 0

```diff
    /// @dev Settles any deltas after adding/removing liquidity
    function _settleDeltas(address sender, PoolKey memory key, BalanceDelta delta) internal {
        key.currency0.settle(poolManager, sender, uint256(int256(-delta.amount0())), false);
        key.currency1.settle(poolManager, sender, uint256(int256(-delta.amount1())), false);
--      if (key.currency0.isAddressZero() || key.currency1.isAddressZero()) _returnNative(sender);
++      if (key.currency0.isAddressZero()) _returnNative(sender);
    }
```

**Paladin:** Acknowledged, change not made.

**Cyfrin:** Acknowledged.
