---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`SettlementBranch::_fillOrder` can revert for positions with negative PNL
  in markets with negative maker/taker fees'
vuln_class: []
---

# `SettlementBranch::_fillOrder` can revert for positions with negative PNL in markets with negative maker/taker fees

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** `SettlementBranch::_fillOrder` calculates the position's PNL as `pnl = (unrealizedPnl + accruedFunding) + (unary(orderFee + settlementFee))`:

```solidity
File: SettlementBranch.sol
141: ctx.pnl = oldPosition.getUnrealizedPnl(ctx.fillPrice).add(
142:     oldPosition.getAccruedFunding(ctx.fundingFeePerUnit)
143:     ).add(unary(ctx.orderFeeUsdX18.add(ctx.settlementFeeUsdX18.intoSD59x18())));
144:
```

If the PNL is negative, `marginToDeductUsdX18` is calculated by deducting the setttlement/order fees.

```solidity
171: if (ctx.pnl.lt(SD_ZERO)) {
172:     UD60x18 marginToDeductUsdX18 = ctx.orderFeeUsdX18.add(ctx.settlementFeeUsdX18.intoSD59x18()).gt(SD_ZERO)
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

As we can see at L183, it assumes `orderFeeUsdX18` could be a negative amount which is possible only when `makerFee/takerFee` is negative.

But during the calculation at L173, it converts `orderFeeUsdX18` to `UD60x18` directly and it will revert with a negative order fee.

```solidity
/// @notice Casts an SD59x18 number into UD60x18.
/// @dev Requirements:
/// - x must be positive.
function intoUD60x18(SD59x18 x) pure returns (UD60x18 result) {
    int256 xInt = SD59x18.unwrap(x);
    if (xInt < 0) {
        revert CastingErrors.PRBMath_SD59x18_IntoUD60x18_Underflow(x);
    }
    result = UD60x18.wrap(uint256(xInt));
}
```

If this revert did not occur, the calculation of `marginToDeductUsdX18` would be incorrect:
```
Normal Case - positive order fee
================================

unrealizedPnl + accruedFunding = -1000, orderFeeUsdX18 = 100, settlementFeeUsdX18 = 200

ctx.pnl = oldPosition.getUnrealizedPnl(ctx.fillPrice).add(
    oldPosition.getAccruedFunding(ctx.fundingFeePerUnit)
).add(unary(ctx.orderFeeUsdX18.add(ctx.settlementFeeUsdX18.intoSD59x18())));

ctx.pnl = -1000 + (unary(100 + 200))
        = -1000 + (unary(300))
        = -1000 - 300
        = -1300

=> ctx.pnl increased by sum of order and settlement fee)


UD60x18 marginToDeductUsdX18 = ctx.orderFeeUsdX18.add(ctx.settlementFeeUsdX18.intoSD59x18()).gt(SD_ZERO)
    ? ctx.pnl.abs().intoUD60x18().sub(ctx.orderFeeUsdX18.intoUD60x18().add(ctx.settlementFeeUsdX18))
    : ctx.pnl.abs().intoUD60x18();

marginToDeductUsdX18 = ctx.pnl.abs().intoUD60x18().sub(ctx.orderFeeUsdX18.intoUD60x18().add(ctx.settlementFeeUsdX18))
                     = 1300 - (100 + 200)
                     = 1300 - 300
                     = 1000

=> marginToDeductUsdX18 equal to original unrealizedPnl+accruedFunding


Edge Case - negative order fee
==============================

unrealizedPnl + accruedFunding = -1000, orderFeeUsdX18 = -100, settlementFeeUsdX18 = 200

ctx.pnl = oldPosition.getUnrealizedPnl(ctx.fillPrice).add(
    oldPosition.getAccruedFunding(ctx.fundingFeePerUnit)
).add(unary(ctx.orderFeeUsdX18.add(ctx.settlementFeeUsdX18.intoSD59x18())));


ctx.pnl = -1000 + (unary(-100 + 200))
        = -1000 + (unary(100))
        = -1000 - 100
        = -1100

=> ctx.pnl decreased by delta between order fee and settlement fee

UD60x18 marginToDeductUsdX18 = ctx.orderFeeUsdX18.add(ctx.settlementFeeUsdX18.intoSD59x18()).gt(SD_ZERO)
    ? ctx.pnl.abs().intoUD60x18().sub(ctx.orderFeeUsdX18.intoUD60x18().add(ctx.settlementFeeUsdX18))
    : ctx.pnl.abs().intoUD60x18();

marginToDeductUsdX18 = ctx.pnl.abs().intoUD60x18().sub(ctx.orderFeeUsdX18.intoUD60x18().add(ctx.settlementFeeUsdX18))
                     = 1100 - (100 + 200) // -100 order fee becomes 100 due to non-reverting `intoUD60x18`
                     = 1100 - 300
                     = 800

=> marginToDeductUsdX18 much lower than what should be deducted
```

**Impact:** `SettlementBranch::_fillOrder` might revert unexpectedly.

**Recommended Mitigation:** It has the same mitigation as another low issue - `SettlementBranch::_fillOrder reverts if absolute value of negative PNL is smaller than sum of order and settlement fees` .

**Zaros:** Fixed in commit [e03228e](https://github.com/zaros-labs/zaros-core/commit/d37c37abab40bfa2320c6925c359faa501577eb3) by no longer supporting negative fees; both `makerFee` and `takerFee` are now unsigned.

**Cyfrin:** Verified.
