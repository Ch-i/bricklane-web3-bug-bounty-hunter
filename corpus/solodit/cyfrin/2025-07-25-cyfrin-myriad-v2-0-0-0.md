---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Ambiguous `-1` return value in `PredictionMarketV3_4::getMarketResolvedOutcome`
vuln_class: []
---

# Ambiguous `-1` return value in `PredictionMarketV3_4::getMarketResolvedOutcome`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** In [`PredictionMarketV3_4::getMarketResolvedOutcome`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L1336-L1345), there is logic to indicate when a market resolution is still pending:

```solidity
function getMarketResolvedOutcome(uint256 marketId) public view returns (int256) {
  Market storage market = markets[marketId];

  // returning -1 if market still not resolved
  if (market.state != MarketState.resolved) {
    return -1;
  }

  return int256(market.resolution.outcomeId);
}
```

The function returns `-1` if the market has not yet reached the `resolved` state. However, if the question is resolved via Reality.eth (Realitio), the returned outcome may be `0xffff...ffff` (`type(uint256).max`), which Reality.eth uses to signal an invalid answer, as noted in their [documentation](https://reality.eth.limo/app/docs/html/contracts.html#fetching-the-answer-to-a-particular-question):

> By convention all supported types use 0xff...ff (aka bytes32(type(uint256).max)) to mean “invalid”.

Because `int256(type(uint256).max)` equals `-1`, a resolved market with an invalid answer will also return `-1` from `getMarketResolvedOutcome()`. This creates ambiguity: services interpreting `-1` as “unresolved” could mistakenly treat an invalid resolution as if the market were still pending.

**Impact:** Consumers relying on `getMarketResolvedOutcome()` to return `-1` only when the market is unresolved may misinterpret the state. A market could be resolved with an invalid answer from Reality.eth, but still appear unresolved due to the reused sentinel value.

**Recommended Mitigation:** Consider returning a different sentinel value to represent unresolved state. Since the number of outcomes is [limited to 32](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L102), any number greater than or equal to 32 could serve as a distinct "unresolved" indicator. However, avoid using `-2`, as it is another [special value](https://github.com/RealityETH/reality-eth-monorepo/blob/0d2dc425f700aaf514f1927384dd6fe0015e8dba/packages/contracts/development/contracts/RealityETH_ERC20-3.0.sol#L26-L28) used by Reality.eth to indicate unresolved answer.

**Myriad:** Fixed in [PR](https://github.com/Polkamarkets/polkamarkets-js/pull/84), commit [`27ccc51`](https://github.com/Polkamarkets/polkamarkets-js/pull/84/commits/27ccc51250696ae5ef379397653d7dd20019529f)

**Cyfrin:** Verified. `-3` is now used as unresolved outcome.
