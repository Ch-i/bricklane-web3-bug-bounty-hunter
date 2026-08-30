---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Calls to `LimitOrderRegistry::cancelOrder` might revert due to overflow
vuln_class: []
---

# Calls to `LimitOrderRegistry::cancelOrder` might revert due to overflow

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** Reasonable input could cause an arithmetic overflow when cancelling orders because large multiplications are performed on variables defined as `uint128` instead of `uint256`. Specifically, when calculating the liquidity percentage to take from a position in `LimitOrderRegistry::cancelOrder`, multiplication of `depositAmount` by `1e18` would cause an overflow when `depositAmount >= 341e18` as the result exceeds the range of `uint128`.

```solidity
uint128 depositAmount = batchIdToUserDepositAmount[batchId][sender];
if (depositAmount == 0) revert LimitOrderRegistry__UserNotFound(sender, batchId);

// Remove one from the userCount.
order.userCount--;

// Zero out user balance.
delete batchIdToUserDepositAmount[batchId][sender];

uint128 orderAmount;
if (order.direction) {
    orderAmount = order.token0Amount;
    if (orderAmount == depositAmount) {
        liquidityPercentToTake = 1e18;
        // Update order tokenAmount.
        order.token0Amount = 0;
    } else {
        liquidityPercentToTake = (1e18 * depositAmount) / orderAmount; // @audit - overflow
        // Update order tokenAmount.
        order.token0Amount = orderAmount - depositAmount;
    }
} else {
    orderAmount = order.token1Amount;
    if (orderAmount == depositAmount) {
        liquidityPercentToTake = 1e18;
        // Update order tokenAmount.
        order.token1Amount = 0;
    } else {
        liquidityPercentToTake = (1e18 * depositAmount) / orderAmount; // @audit - overflow
        // Update order tokenAmount.
        order.token1Amount = orderAmount - depositAmount;
    }
}
```

**Impact:** It can become impossible for a user to cancel their order if their deposit amount equals or exceeds `341e18`, unless they are the final depositor to the pool.

**Recommended Mitigation:**
```solidity
liquidityPercentToTake = (1e18 * uint256(depositAmount)) / orderAmount;
```

**GFX Labs:** Fixed by casting `depositAmount` as a `uint256` in commit [d67b293](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/d67b293afbe3590ddb835fc2f9ec617d056cb3c2).

**Cyfrin:** Acknowledged.
