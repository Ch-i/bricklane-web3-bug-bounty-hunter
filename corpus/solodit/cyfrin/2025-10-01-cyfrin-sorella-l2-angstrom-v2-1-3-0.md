---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Custom error conditionals can be re-written for better readability
vuln_class: []
---

# Custom error conditionals can be re-written for better readability

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** In numerous instances throughout the contracts, the `!(... <binary comparison operator> ...)` pattern is used when reverting with custom errors. By De Morgan's Laws, such conditionals can be re-written for better readability.

**Recommended Mitigation:** * `UniConsumer.sol`:
```diff
function _onlyUniV4() internal view {
-   if (!(msg.sender == address(UNI_V4))) revert NotUniswap();
+   if (msg.sender != address(UNI_V4)) revert NotUniswap();
}
```

* `TickIterator.sol`:
```diff
function reset(TickIteratorUp memory self, int24 startTick) internal view {
-   if (!(startTick <= self.endTick)) revert InvalidRange();
+   if (startTick > self.endTick) revert InvalidRange();
    ...
}

function reset(TickIteratorDown memory self, int24 startTick) internal view {
-   if (!(self.endTick <= startTick)) revert InvalidRange();
+   if (self.endTick > startTick) revert InvalidRange();
    ...
}
```

* `Math512Lib.sol`:
```diff
function checkedMul2Pow192(uint256 x1, uint256 x0)
    internal
    pure
    returns (uint256 y1, uint256 y0)
{
-   if (!((x1 << 192) >> 192 == x1)) revert Overflow();
+   if ((x1 << 192) >> 192 != x1) revert Overflow();
    return ((x1 << 192) | (x0 >> 64), x0 << 192);
}

function checkedMul2Pow96(uint256 x1, uint256 x0)
    internal
    pure
    returns (uint256 y1, uint256 y0)
{
-   if (!((x1 << 96) >> 96 == x1)) revert Overflow();
+   if ((x1 << 96) >> 96 != x1) revert Overflow();
    return ((x1 << 96) | (x0 >> 160), x0 << 96);
}
```

* `PoolRewards.sol`:
```diff
// updateAfterLiquidityAdd()
-   if (!(params.liquidityDelta >= 0)) revert NegativeDeltaForAdd();
+   if (params.liquidityDelta < 0) revert NegativeDeltaForAdd();

// updateAfterLiquidityRemove()
-   if (!(0 >= params.liquidityDelta)) revert PositiveDeltaForRemove();
+   if (params.liquidityDelta > 0)) revert PositiveDeltaForRemove();
```

* `AngstromL2.sol`:
```diff
function withdrawProtocolRevenue(uint160 assetId, address to, uint256 amount) public {
    _checkOwner();

    if (assetId == NATIVE_CURRENCY_ID) {
-       if (!(amount <= unclaimedProtocolRevenueInEther)) {
+       if (amount > unclaimedProtocolRevenueInEther) {
            revert AttemptingToWithdrawLPRewards();
        }
        unclaimedProtocolRevenueInEther -= amount.toUint128();
    }

    UNI_V4.transfer(to, assetId, amount);
}

...

function setPoolHookSwapFee(PoolKey calldata key, uint256 newFeeE6) public {
    _checkOwner();
-   if (!(newFeeE6 <= MAX_PROTOCOL_FEE_E6)) revert ProtocolFeeExceedsMaximum();
+   if (newFeeE6 > MAX_PROTOCOL_FEE_E6) revert ProtocolFeeExceedsMaximum();
    ...
}
```

**Sorella Labs:** Acknowledged. As discussed, this is my own quirky style which I deem more readable because it makes the inner condition be that which you would put inside an assert or require which I personally find more intuitive.

**Cyfrin:** Acknowledged.
