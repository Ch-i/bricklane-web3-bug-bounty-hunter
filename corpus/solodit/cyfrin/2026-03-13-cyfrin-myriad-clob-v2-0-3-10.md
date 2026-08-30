---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-10
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`NegRiskAdapter::createEvent` allows different `closesAt` across outcome markets'
vuln_class: []
---

# `NegRiskAdapter::createEvent` allows different `closesAt` across outcome markets

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `NegRiskAdapter::createEvent` iterates over caller-supplied `marketParams` and creates one market per outcome via `manager.createNegRiskMarket`. There is no validation that all `marketParams[i].closesAt` values are identical:

```solidity
for (uint256 i = 0; i < marketParams.length; i++) {
    uint256 marketId = manager.createNegRiskMarket(marketParams[i], IERC20(address(wcol)), eventId);
    evt.marketIds.push(marketId);
}
```

`MyriadCTFExchange::matchCrossMarketOrders` calls `_requireMarketOpen` for every order in the batch. The moment the earliest-closing market transitions to `closed`, any cross-market fill for the event reverts:

```solidity
require(manager.getMarketState(marketId) == MarketState.open, "market closed");
```

Users holding YES positions in the still-open markets lose their primary exit mechanism (cross-market matching) before the event has actually concluded.

**Recommended Mitigation:** Enforce uniform close times in `createEvent`:

```solidity
uint256 closesAt = marketParams[0].closesAt;
for (uint256 i = 1; i < marketParams.length; i++) {
    require(marketParams[i].closesAt == closesAt, "closesAt mismatch");
}
```

**Myriad:** Fixed in commit [`9a77afb`](https://github.com/Polkamarkets/polkamarkets-js/commit/9a77afb38be03035a2cdd2b44393b288188f9c00)

**Cyfrin:** Verified.
