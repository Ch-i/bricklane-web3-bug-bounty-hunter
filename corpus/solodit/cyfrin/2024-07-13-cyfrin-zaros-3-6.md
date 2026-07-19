---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-3-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Liquidation reverts if collateral price feed returns 0
vuln_class: []
---

# Liquidation reverts if collateral price feed returns 0

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Liquidation reverts if collateral price feed returns 0. Generally this should never happen as Chainlink price feeds have a `minAnswer` they should always at least return. However since a trader can have a basket of different collateral, it may be worth handling this edge case and trying to liquidate other collateral.

**Proof of Concept:** Add the following PoC to `test/integration/perpetuals/liquidation-branch/liquidateAccounts/liquidateAccounts.t.sol`:
```solidity
function test_LiquidationRevertsWhenPriceFeedReturnsZero() external {
    // give naruto some wstEth to deposit as collateral
    uint256 USER_STARTING_BALANCE = 1e18;
    int128  USER_POS_SIZE_DELTA   = 1e18;
    deal({ token: address(mockWstEth), to: users.naruto, give: USER_STARTING_BALANCE });

    // naruto creates a trading account and deposits their tokens as collateral
    changePrank({ msgSender: users.naruto });
    uint128 tradingAccountId = createAccountAndDeposit(USER_STARTING_BALANCE, address(mockWstEth));

    // naruto opens first position in BTC market
    openManualPosition(BTC_USD_MARKET_ID, BTC_USD_STREAM_ID, MOCK_BTC_USD_PRICE, tradingAccountId, USER_POS_SIZE_DELTA);

    // price of naruto's collateral has a LUNA-like crash
    // this code occur while the L2 stopped producing blocks
    // as recently happened during the Linea hack such that
    // the liquidation bots could not perform a timely
    // liquidation of the position
    MockPriceFeed wstEthPriceFeed = mockPriceAdapters.mockWstEthUsdPriceAdapter;
    wstEthPriceFeed.updateMockPrice(0);

    // verify naruto can now be liquidated
    uint128[] memory liquidatableAccountsIds = perpsEngine.checkLiquidatableAccounts(0, 1);
    assertEq(1, liquidatableAccountsIds.length);
    assertEq(tradingAccountId, liquidatableAccountsIds[0]);

    // attempt to liquidate naruto
    changePrank({ msgSender: liquidationKeeper });
    // reverts with `panic: division or modulo by zero`
    perpsEngine.liquidateAccounts(liquidatableAccountsIds, users.settlementFeeRecipient);
}
```

Run with: `forge test --match-test test_LiquidationRevertsWhenPriceFeedReturnsZero -vvv`

**Zaros:** Acknowledged; very unlikely to occur since Chainlink price feeds have in-built minimum prices they will return which are typically > 0.

\clearpage
