---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Perform additional validation on Chainlink fast gas feed
vuln_class: []
---

# Perform additional validation on Chainlink fast gas feed

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** When consuming data feeds provided by Chainlink, it is important to validate a number of thresholds and return values. Without this, it is possible for a consuming contract to use stale or otherwise incorrect/invalid data. `LimitOrderRegistry` currently correctly validates the time since the last update against an owner-specified heartbeat value; however, it is possible to perform additional validation to ensure that the returned gas price is indeed valid, for example within upper/lower bounds and the result of a complete reporting round.

**Impact:** `LimitOrderRegistry::performUpkeep` is reliant on this functionality within `LimitOrderRegistry::getGasPrice` which could result in DoS on fulfilling orders if not functioning correctly; however, the escape-hatch is simply having the owner set the feed address to `address(0)` which causes the owner-specified fallback value to be used.

**Recommended Mitigation:** Consider calling `IChainlinkAggregator::latestRoundData` within a `try/catch` block and include the following additional validation:

```solidity
require(signedGasPrice > 0, "Negative gas price");
require(signedGasPrice < maxGasPrice, "Upper gas price bound breached");
require(signedGasPrice > minGasPrice, "Lower gas price bound breached");
require(answeredInRound >= roundID, "Round incomplete");
```

**GFX Labs:** Acknowledged. Chainlink has an outstanding track record for their data feed accuracy and reliability, and if Chainlink nodes did want to start maliciously reporting incorrect values, there are significantly more profitable opportunities elsewhere.

Also, in the event of the fast gas feed becoming unreliable, the owner can either manually set the gas price, or it would be straightforward to make a custom Fast Gas Feed contract that is updated by a GFX Labs bot.

**Cyfrin:** Acknowledged.
