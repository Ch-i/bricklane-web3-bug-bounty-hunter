---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Markets Stuck in 'Open' State even if `block.timestamp > markets[marketId].closesAtTimestamp
  == true`
vuln_class: []
---

# Markets Stuck in 'Open' State even if `block.timestamp > markets[marketId].closesAtTimestamp == true`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** Functions  `_buy`, `_sell`, `_addLiquidity` or `_removeLiquidity` use the `timeTransitions(marketId)` modifier followed by `atState(marketId, MarketState.open)`.

If someone tries to do one of these operations in this context: `block.timestamp > markets[marketId].closesAtTimestamp && markets[marketId].state == MarketState.open` then the code calls `_nextState(marketId)` which changes the state from `open` to `closed`: `market.state = MarketState(uint256(market.state) + 1)`. But when the next modifier runs atState(marketId, MarketState.open) everything reverts. The market state change doesn't persist, leaving the `markets[marketId].state = MarketState.open`.

Furthermore, the only time when `timeTransitions` successfully executes the `_nextState` transition, in that context, is inside `resolveMarketOutcome`. Making the `closed` state only a transitory step between `open` and `resolved` that takes place between the execution of `resolveMarketOutcome` function's modifiers.

**Impact:** Markets remain in `open` state even if `block.timestamp > markets[marketId].closesAtTimestamp == true` when they should be closed, possibly causing UX issues.

Any tx attempting to `_buy`, `_sell`, `_addLiquidity` or `_removeLiquidity` will get reverted by the `atState(marketId, MarketState.open)` modifier, wasting caller's gas.

**Proof of Concept:** Add the following test inside `PredictionMarket.t.sol`:
```solidity
    function test_MarketStuckInOpenState() public {
        // Create market that closes in 1 hour
        uint32 closeTime = uint32(block.timestamp + 3600);

        PredictionMarketV3_4.CreateMarketDescription memory desc = PredictionMarketV3_4.CreateMarketDescription({
            value: VALUE,
            closesAt: closeTime,
            outcomes: 2,
            token: IERC20(address(tokenERC20)),
            distribution: new uint256[](0),
            question: "PoC Market State Issue",
            image: "test",
            arbitrator: address(0x1),
            buyFees: PredictionMarketV3_4.Fees({fee: 0, treasuryFee: 0, distributorFee: 0}),
            sellFees: PredictionMarketV3_4.Fees({fee: 0, treasuryFee: 0, distributorFee: 0}),
            treasury: treasury,
            distributor: distributor,
            realitioTimeout: 3600,
            manager: IPredictionMarketV3Manager(address(manager))
        });

        uint256 marketId = predictionMarket.createMarket(desc);

        // Verify market is initially open
        (PredictionMarketV3_4.MarketState state, uint256 closesAt,,,,) = predictionMarket.getMarketData(marketId);
        assertEq(uint256(state), uint256(PredictionMarketV3_4.MarketState.open));
        assertEq(closesAt, closeTime);

        console.log("BEFORE TIME WARP");
        console.log("Market state (0=open, 1=closed, 2=resolved):", uint256(state));
        console.log("Time until close:", closesAt - block.timestamp);

        // TIME WARP: Move 2 hours into the future (1 hour past close time)
        vm.warp(block.timestamp + 7200);

        console.log("AFTER TIME WARP");
        console.log("Market closes at:", closesAt);
        console.log("Time past close:", block.timestamp - closesAt);

        (state,,,,,) = predictionMarket.getMarketData(marketId);
        console.log("Market state (should be 1=closed, but shows):", uint256(state));

        // Prove the market is logically closed but state is wrong
        assertTrue(block.timestamp > closesAt, "We are past close time");
        assertEq(uint256(state), uint256(PredictionMarketV3_4.MarketState.open), "Market incorrectly shows as open!");

        // ATTEMPT TO TRADE: This should fail due to modifier ordering issue
        console.log("ATTEMPTING TRADE (should fail)");

        address trader = makeAddr("trader");
        deal(address(tokenERC20), trader, 1 ether);

        vm.startPrank(trader);
        tokenERC20.approve(address(predictionMarket), type(uint256).max);
        vm.expectRevert(bytes("!ms")); // Market state error
        predictionMarket.buy(marketId, 0, 0, 0.1 ether);
        vm.stopPrank();

        console.log("Trade failed as expected due to modifier");
    }
```

**Recommended Mitigation:** Consider removing the state `closed` and using the `closesAtDate` to indicate whether the market is open/closed, or make the transition work.

**Myriad:** Fixed in [PR#85](https://github.com/Polkamarkets/polkamarkets-js/pull/85), commit [`627d5be`](https://github.com/Polkamarkets/polkamarkets-js/pull/85/commits/627d5be4f706f6d96bdfad924d26ed83c322317b)

**Cyfrin:** Verified. `getMarketData` now calls a new function `getMarketState` which returns `closed` if `market.state == MarketState.open && block.timestamp >= market.closesAtTimestamp`.
