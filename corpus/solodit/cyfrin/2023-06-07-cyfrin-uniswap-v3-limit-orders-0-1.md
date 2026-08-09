---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: New orders on a given pool in the opposite direction, separated by zero/one
  tick space, are not possible until previous `BatchOrder` is removed from the order
  book
vuln_class: []
---

# New orders on a given pool in the opposite direction, separated by zero/one tick space, are not possible until previous `BatchOrder` is removed from the order book

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** New order creation will revert with `LimitOrderRegistry__DirectionMisMatch()` if the direction opposes any existing orders at the current tick price. Due to the calculation of lower/upper ticks, this also applies to orders separated by one tick space. In the event price deviation causes existing orders to become ITM, it is not possible to place new orders in the opposing direction until upkeep has been performed for the existing orders, fully removing them from the order book.

**Impact:** This edge case is only an issue in the following circumstance:
* Any number of users place an order at a given tick price.
* Price deviates, causing this `BatchOrder` (and potentially others) to become ITM.
* If upkeep has not yet been performed, either through DoS, oracle downtime, or exceeding the maximum number of orders per upkeep (in the case of very large price deviations), the original `BatchOrder` remains on the order book (represented by a doubly linked list).
* So long as the original order remains in the list, new orders on a given pool in the opposite direction, separated by zero/one tick space, cannot be placed.

**Proof of Concept:**
```solidity
function testOppositeOrders() external {
    uint256 amount = 1_000e6;
    deal(address(USDC), address(this), amount);

    // Current tick 204332
    // 204367
    // Current block 16371089
    USDC.approve(address(registry), amount);
    registry.newOrder(USDC_WETH_05_POOL, 204910, uint96(amount), true, 0);

    // Make a large swap to move the pool tick.
    address[] memory path = new address[](2);
    path[0] = address(WETH);
    path[1] = address(USDC);

    uint24[] memory poolFees = new uint24[](1);
    poolFees[0] = 500;

    (bool upkeepNeeded, bytes memory performData) = registry.checkUpkeep(abi.encode(USDC_WETH_05_POOL));

    uint256 swapAmount = 2_000e18;
    deal(address(WETH), address(this), swapAmount);
    _swap(path, poolFees, swapAmount);

    (upkeepNeeded, performData) = registry.checkUpkeep(abi.encode(USDC_WETH_05_POOL));

    assertTrue(upkeepNeeded, "Upkeep should be needed.");

    // registry.performUpkeep(performData);

    amount = 2_000e17;
    deal(address(WETH), address(this), amount);
    WETH.approve(address(registry), amount);
    int24 target = 204910 - USDC_WETH_05_POOL.tickSpacing();
    vm.expectRevert(
        abi.encodeWithSelector(LimitOrderRegistry.LimitOrderRegistry__DirectionMisMatch.selector)
    );
    registry.newOrder(USDC_WETH_05_POOL, target, uint96(amount), false, 0);
}
```

**Recommended Mitigation:** Implement a second order book for orders in the opposite direction, as discussed.

**GFX Labs:** Fixed by separating the order book into two lists, and having orders in opposite directions use completely different LP positions in commits [7b65915](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/7b6591508cc0f412edd7f105f012a0cbb7f4b1fe) and [9e9ceda](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/9e9cedad083ff9812a9782a88ac9db5cd713b743).

**Cyfrin:** Acknowledged. Comment should be updated for `getPositionFromTicks` mapping to include 'direction' key.

**GFX Labs:** Fixed in commit [f303a50](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/f303a502492aaf31aeb180640861f326039dd962).

**Cyfrin:** Acknowledged.
