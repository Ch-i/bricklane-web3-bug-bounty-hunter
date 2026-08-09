---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`PerpMarket::getOrderFeeUsd` incorrectly charges `makerFee` when skew is zero
  and trade is buy order'
vuln_class: []
---

# `PerpMarket::getOrderFeeUsd` incorrectly charges `makerFee` when skew is zero and trade is buy order

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** In `PerpMarket::getOrderFeeUsd` there is this comment to which I've added (*) at the end:
```solidity
/// @dev When the skew is zero, taker fee will be charged. (*)
```

But doing a truth table for the `if` statement's boolean expression shows this comment is not always true:
```solidity
// isSkewGtZero = true,  isBuyOrder = true  -> taker fee
// isSkewGtZero = true,  isBuyOrder = false -> maker fee
// isSkewGtZero = false, isBuyOrder = true  -> maker fee (*)
// isSkewGtZero = false, isBuyOrder = false -> taker fee
if (isSkewGtZero != isBuyOrder) {
    // not equal charge maker fee
    feeBps = sd59x18((self.configuration.orderFees.makerFee));
} else {
    // equal charge taker fee
    feeBps = sd59x18((self.configuration.orderFees.takerFee));
}
```

When `isSkewGtZero == false && isBuyOrder = true`, the *maker* fee will be charged, even though the skew is zero and hence this order is causing the skew. This behavior is the opposite of what the comment says should happen, and logically the *taker* fee should be charged if the trade causes the skew.

**Impact:** Incorrect fee is charged.

**Recommended Mitigation:** When `isSkewGtZero == false && isBuyOrder = true` the *taker* fee should be charged since the trader is causing the skew.

**Zaros:** Fixed in commits [534b089](https://github.com/zaros-labs/zaros-core/commit/534b0891d836e1cd01daf808f72c39269aa213ae) and [5822b19](https://github.com/zaros-labs/zaros-core/commit/5822b19b987b23fb3373afc0fb3e7a30441cdd01).

**Cyfrin:** Verified.
