---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`SettlementBranch::_fillOrder` reverts if absolute value of PNL is smaller
  than sum of order and settlement fees'
vuln_class: []
---

# `SettlementBranch::_fillOrder` reverts if absolute value of PNL is smaller than sum of order and settlement fees

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** `SettlementBranch::_fillOrder` calculates the position's PNL as `pnl = unrealizedPnl + accruedFunding + unary(orderFee + settlementFee)`:

```solidity
File: SettlementBranch.sol
141: ctx.pnl = oldPosition.getUnrealizedPnl(ctx.fillPrice).add(
142:     oldPosition.getAccruedFunding(ctx.fundingFeePerUnit)
143:     ).add(unary(ctx.orderFeeUsdX18.add(ctx.settlementFeeUsdX18.intoSD59x18())));
144:
```

If PNL is positive and unrealized_pnl + accrued_funding < order_fee + settlement_fee this will revert due to underflow.

If the PNL is negative an amount is deduced from the account's margin:

```solidity
171: if (ctx.pnl.lt(SD_ZERO)) {
172:     UD60x18 marginToDeductUsdX18 = ctx.orderFeeUsdX18.add(ctx.settlementFeeUsdX18.intoSD59x18()).gt(SD_ZERO)
         // @audit can revert with underflow if abs(pnl) < order_fee+settlement_fee
173:     ? ctx.pnl.abs().intoUD60x18().sub(ctx.orderFeeUsdX18.intoUD60x18().add(ctx.settlementFeeUsdX18))
174:     : ctx.pnl.abs().intoUD60x18();
175:
176:     tradingAccount.deductAccountMargin({
177:         feeRecipients: FeeRecipients.Data({
178:         marginCollateralRecipient: globalConfiguration.marginCollateralRecipient,
179:         orderFeeRecipient: globalConfiguration.orderFeeRecipient,
180:         settlementFeeRecipient: globalConfiguration.settlementFeeRecipient
181:     }),
182:     pnlUsdX18: marginToDeductUsdX18,
183:     orderFeeUsdX18: ctx.orderFeeUsdX18.gt(SD_ZERO) ? ctx.orderFeeUsdX18.intoUD60x18() : UD_ZERO,
184:     settlementFeeUsdX18: ctx.settlementFeeUsdX18
185:     });
```

The first condition of the `marginToDeductUsdX18` calculation at L173 will revert due to underflow if:
* the trader has a loss (negative PNL)
* the absolute value of the loss is smaller than the sum of the order/settlement fees

**Proof of Concept:** Add the following PoCs to `test/integration/perpetuals/order-branch/createMarketOrder/createMarketOrder.t.sol`:
```solidity
function test_OrderRevertsUnderflowWhenPositivePnlLessThanFees() external {
    // give naruto some tokens
    uint256 USER_STARTING_BALANCE = 100_000e18;
    int128  USER_POS_SIZE_DELTA   = 0.002e18;
    deal({ token: address(usdToken), to: users.naruto, give: USER_STARTING_BALANCE });

    // naruto creates a trading account and deposits their tokens as collateral
    changePrank({ msgSender: users.naruto });
    uint128 tradingAccountId = createAccountAndDeposit(USER_STARTING_BALANCE, address(usdToken));

    // naruto opens position in BTC market
    openManualPosition(BTC_USD_MARKET_ID, BTC_USD_STREAM_ID, MOCK_BTC_USD_PRICE, tradingAccountId, USER_POS_SIZE_DELTA);

    // market moves slightly against Naruto's position
    // giving Naruto's position a slightly negative PNL
    updateMockPriceFeed(BTC_USD_MARKET_ID, MOCK_BTC_USD_PRICE+1);

    // naruto attempts to close their position
    changePrank({ msgSender: users.naruto });

    // reverts due to underflow
    openManualPosition(BTC_USD_MARKET_ID, BTC_USD_STREAM_ID, MOCK_BTC_USD_PRICE, tradingAccountId, -USER_POS_SIZE_DELTA/2);
}

function test_OrderRevertsUnderflowWhenNegativePnlLessThanFees() external {
    // give naruto some tokens
    uint256 USER_STARTING_BALANCE = 100_000e18;
    int128  USER_POS_SIZE_DELTA   = 0.002e18;
    deal({ token: address(usdToken), to: users.naruto, give: USER_STARTING_BALANCE });

    // naruto creates a trading account and deposits their tokens as collateral
    changePrank({ msgSender: users.naruto });
    uint128 tradingAccountId = createAccountAndDeposit(USER_STARTING_BALANCE, address(usdToken));

    // naruto opens position in BTC market
    openManualPosition(BTC_USD_MARKET_ID, BTC_USD_STREAM_ID, MOCK_BTC_USD_PRICE, tradingAccountId, USER_POS_SIZE_DELTA);

    // market moves slightly against Naruto's position
    // giving Naruto's position a slightly negative PNL
    updateMockPriceFeed(BTC_USD_MARKET_ID, MOCK_BTC_USD_PRICE-1);

    // naruto attempts to partially close their position
    changePrank({ msgSender: users.naruto });

    // reverts due to underflow
    openManualPosition(BTC_USD_MARKET_ID, BTC_USD_STREAM_ID, MOCK_BTC_USD_PRICE, tradingAccountId, -USER_POS_SIZE_DELTA/2);
}
```

Run with:
* `forge test --match-test test_OrderRevertsUnderflowWhenPositivePnlLessThanFees -vvv`
* `forge test --match-test test_OrderRevertsUnderflowWhenNegativePnlLessThanFees -vvv`

**Recommended Mitigation:** Refactor how old position PNL is settled and  order/settlement fees are paid.

**Zaros:** Fixed in commit [516bc2a](https://github.com/zaros-labs/zaros-core/commit/516bc2ad61d64e94654db500a93bd19567ca01e5).

**Cyfrin:** Verified.
