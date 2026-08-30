---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-4-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`MyriadCTFExchange::_requireMarketOpen` makes two external calls to `manager`'
vuln_class: []
---

# `MyriadCTFExchange::_requireMarketOpen` makes two external calls to `manager`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `MyriadCTFExchange::_requireMarketOpen` issues two separate external calls to `manager` on every invocation:

```solidity
function _requireMarketOpen(uint256 marketId) internal view {
    require(manager.getMarketState(marketId) == IMyriadMarketManager.MarketState.open, "market closed");
    require(!manager.isMarketPaused(marketId), "market paused");
}
```

Each external call costs at minimum 100 gas (warm) or 2100 gas (cold) for the `CALL` opcode. `_requireMarketOpen` is called once per order in `matchCrossMarketOrders` (N times for an N-outcome event) and once per `_matchOrders` call in the single-market path, making the overhead cumulative.

**Recommended Mitigation:** Add a combined view function to `IMyriadMarketManager` and its implementation:

```solidity
function isMarketTradeable(uint256 marketId) external view returns (bool) {
    Market storage m = markets[marketId];
    return m.state == MarketState.open && !m.paused;
}
```

Then simplify `_requireMarketOpen` to a single external call:

```solidity
function _requireMarketOpen(uint256 marketId) internal view {
    require(manager.isMarketTradeable(marketId), "market not tradeable");
}
```

**Myriad:** Fixed in commit [`b3e2586`](https://github.com/Polkamarkets/polkamarkets-js/commit/b3e2586a797a3c2e2fb388d4ff1a733b2350a36a)

**Cyfrin:** Verified.
