---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: NegRisk market creator is set to adapter address instead of the initiator
vuln_class: []
---

# NegRisk market creator is set to adapter address instead of the initiator

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `PredictionMarketV3ManagerCLOB::createNegRiskMarket` is restricted to the registered `NegRiskAdapter`. When the adapter creates a neg-risk event it calls the manager in a loop; inside the manager we set `market.creator = msg.sender`. At that point `msg.sender` is the adapter contract, not the address that called the adapter. So every neg-risk market ends up with `creator` equal to the adapter, and the actual initiator (the market admin who called `NegRiskAdapter::createEvent`) is not recorded.

This matters for any logic or UI that treats `creator` as the human or admin who created the market — for example display, permissions, or analytics. For neg-risk markets that information is wrong.

```solidity
// PredictionMarketV3ManagerCLOB.sol:129-154
function createNegRiskMarket(
  CreateMarketParams calldata params,
  IERC20 collateralOverride,
  bytes32 eventId
) external nonReentrant returns (uint256 marketId) {
  require(msg.sender == negRiskAdapter, "not adapter");
  // ...
  market.creator = msg.sender;  // adapter, not the EOA/admin who called the adapter
```

**Recommended Mitigation:** Pass the actual creator into `createNegRiskMarket` and use it for `market.creator`. Also consider adding the creator to the `MarketCreated` event.

**Myriad:** Fixed in commit [`285a63c`](https://github.com/Polkamarkets/polkamarkets-js/commit/285a63c7a7bdbb10ac3604855cc1e216b1343b3d)

**Cyfrin:** Verified.
