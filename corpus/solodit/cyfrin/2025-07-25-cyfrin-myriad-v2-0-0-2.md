---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Operations done right at the `closesAtTimestamp`
vuln_class: []
---

# Operations done right at the `closesAtTimestamp`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** The protocol checks the time validity of all user facing methods through the following modifier:

```solidity
  modifier timeTransitions(uint256 marketId) {
    if (block.timestamp > markets[marketId].closesAtTimestamp && markets[marketId].state == MarketState.open) {
      _nextState(marketId);
    }
    _;
  }
```

This condition `block.timestamp > markets[marketId].closesAtTimestamp` excludes the case where `block.timestamp = markets[marketId].closesAtTimestamp`, allowing buy, sell, addLiquidity and removeLiquidity operations right on market closure.

**Impact:** Potential risk free earnings depending on the market status and correct answer.

**Proof of Concept:** Add the following to `PredictionMarket.t.sol`

```solidity
    function testTradeRightAtMarketClose() public {
        uint256 marketId = _createTestMarket();

        // Get market close time
        (,uint256 closesAt,,,,) = predictionMarket.getMarketData(marketId);

        // Set timestamp to exact close time
        vm.warp(closesAt);

        // This should fail - market transitions to closed due to timeTransitions modifier // NB it doesn't
        // vm.expectRevert(bytes("!ms")); // Market state error
        predictionMarket.buy(marketId, 0, 0, VALUE);
    }


    function testLiquidityOperationsAtMarketClose() public {
        uint256 marketId = _createTestMarket();

        // Get market close time
        (,uint256 closesAt,,,,) = predictionMarket.getMarketData(marketId);

        // Add more liquidity before close
        vm.warp(closesAt - 1);
        predictionMarket.addLiquidity(marketId, VALUE);

        // Try to add liquidity at exact close time - should fail // NB it doesn't
        vm.warp(closesAt);
        // vm.expectRevert(bytes("!ms"));
        predictionMarket.addLiquidity(marketId, VALUE);
    }
```

**Recommended Mitigation:**
```diff
  modifier timeTransitions(uint256 marketId) {
--    if (block.timestamp > markets[marketId].closesAtTimestamp && markets[marketId].state == MarketState.open) {
++    if (block.timestamp >= markets[marketId].closesAtTimestamp && markets[marketId].state == MarketState.open) {
      _nextState(marketId);
    }
    _;
  }
```


**Myriad:** Fixed in [PR#79](https://github.com/Polkamarkets/polkamarkets-js/pull/79), commit [`774161e`](https://github.com/Polkamarkets/polkamarkets-js/pull/79/commits/774161e4d0a1ab16a38d6b7eda97534bce9e1f94)

**Cyfrin:** Verified. Check is now `>=`.
