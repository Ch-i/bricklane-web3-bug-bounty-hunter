---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-4-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`MyriadCTFExchange.filledAmounts` mapping slot and `hashOrder` computed multiple
  times per order'
vuln_class: []
---

# `MyriadCTFExchange.filledAmounts` mapping slot and `hashOrder` computed multiple times per order

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** In `MyriadCTFExchange::_matchOrders` (the inner settlement function called by every `matchOrdersWithFees` invocation), each order's `filledAmounts` slot is read three times:

```
line 360: require(filledAmounts[makerHash] + fillAmount <= maker.amount, …)  // cold SLOAD
line 366: filledAmounts[makerHash] += fillAmount;                             // warm SLOAD + SSTORE
line 389: emit OrdersMatched(…, filledAmounts[makerHash], …)                 // warm SLOAD
```

The same pattern applies to `takerHash`.

In `MyriadCTFExchange::matchCrossMarketOrders`, the problem compounds across N orders: `hashOrder(orders[i])` is computed in both the validation loop (line 242) and the distribution loop (line 295), and `filledAmounts[orderHash]` is read in the validation loop (line 243), then read-modified-written in the distribution loop (line 296), then read again for the emit (line 298).

**Recommended Mitigation:** Cache each value after its first read:

```solidity
// _matchOrders
uint256 makerFilled = filledAmounts[makerHash];
uint256 takerFilled = filledAmounts[takerHash];
require(makerFilled + fillAmount <= maker.amount, "maker overfill");
require(takerFilled + fillAmount <= taker.amount, "taker overfill");
makerFilled += fillAmount;
takerFilled += fillAmount;
filledAmounts[makerHash] = makerFilled;
filledAmounts[takerHash] = takerFilled;
// use makerFilled / takerFilled in the emit

// matchCrossMarketOrders — first loop: cache hash and current fill
bytes32[] memory orderHashes   = new bytes32[](orders.length);
uint256[] memory currentFilled = new uint256[](orders.length);
for (uint256 i = 0; i < orders.length; i++) {
    bytes32 h = hashOrder(orders[i]);
    orderHashes[i]   = h;
    currentFilled[i] = filledAmounts[h];
    require(currentFilled[i] + fillAmount <= orders[i].amount, "overfill");
    …
}
// second loop: use cached values
for (uint256 i = 0; i < orders.length; i++) {
    uint256 newFill = currentFilled[i] + fillAmount;
    filledAmounts[orderHashes[i]] = newFill;
    emit CrossMarketOrderFilled(orderHashes[i], eventId, orders[i].marketId, fillAmount, newFill);
}
```

**Myriad:** Fixed in commit [`968ca58`](https://github.com/Polkamarkets/polkamarkets-js/commit/968ca583d63c14f53b6cefcd192cee98e08a1bbe)

**Cyfrin:** Verified.

\clearpage
