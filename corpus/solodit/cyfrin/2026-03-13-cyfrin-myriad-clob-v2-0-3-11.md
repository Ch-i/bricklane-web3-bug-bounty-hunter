---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-11
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Market pause flag not enforced by `ConditionalTokens::splitPosition`
vuln_class: []
---

# Market pause flag not enforced by `ConditionalTokens::splitPosition`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `PredictionMarketV3ManagerCLOB::pauseMarket` sets a per-market `paused` flag. The exchange respects this via `_requireMarketOpen` -> `manager.isMarketPaused`. However, `ConditionalTokens::splitPosition` checks only the market state, not the pause flag:

```solidity
// ConditionalTokens.sol:34
require(manager.getMarketState(marketId) == IMyriadMarketManager.MarketState.open, "market not open");
// isMarketPaused is never checked
```

Any user can call `ConditionalTokens::splitPosition` directly to acquire fresh YES/NO tokens on a market the admin intended to freeze, bypassing the pause entirely. During an incident pause (e.g. ahead of an emergency void), new exposure can still be created.

**Recommended Mitigation:** Add a pause guard to `ConditionalTokens::splitPosition`:

```solidity
require(!manager.isMarketPaused(marketId), "market paused");
```

**Myriad:** Fixed in commit [`8be2650`](https://github.com/Polkamarkets/polkamarkets-js/commit/8be265059802e5e1e79bca4286d17616be90c47f)

**Cyfrin:** Verified.
