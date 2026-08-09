---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`ChainlinkUpDownAdapter::emergencyCloseRounds` accepts empty price array and
  negative prices'
vuln_class: []
---

# `ChainlinkUpDownAdapter::emergencyCloseRounds` accepts empty price array and negative prices

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `ChainlinkUpDownAdapter::emergencyCloseRounds` is gated by `EMERGENCY_CLOSE_ROUND_ROLE` but has two input validation gaps that can cause incorrect or silent settlement during an emergency:

  **1. Empty `endPrices[]` array is a silent no-op**

  ```solidity
  for (uint32 i = 0; i < endPrices.length; i++) { ... }
```
Passing an empty array causes the loop body to never execute. The function returns with no revert, no event, and no rounds closed. An operator under time pressure may not notice.

**2. Negative endPrices[i] forces deterministic Down outcome**

```
  _closeRound checks endPrice == 0 but not endPrice < 0:

  if (endPrice == 0) revert
  ChainlinkUpDownAdapter__EndPriceCannotBeZero();
  // no guard on negative values
```

A negative `endPrice` paired with any positive stored `startPrice` evaluates `startPrice > endPrice` → Down, regardless of actual market movement. This flips every round in the batch to Down via an admin typo.

The same gap exists in _closeRound itself; there is no `startPrice > 0` guard either. This is currently benign for BTC/ETH (Data Streams V3 cannot emit negative prices for spot feeds), but becomes load-bearing once rate or index feeds are added to the roster, since `int192` supports negative values and rate feeds can legitimately go negative.

Because only the role-holder can trigger this, the scenario could be a honest admin typo during a high-pressure emergency, not unprivileged exploitation.

**Impact:**
  - Empty `endPrices[]`: silent failure - operator believes rounds are settled, they are not
  - Negative `endPrice`: all rounds in the batch settle as Down regardless of actual price movement

**Recommended Mitigation:** Add guards at the top of `emergencyCloseRounds` and strengthen `_closeRound`:

```solidity
  function emergencyCloseRounds(
      bytes32 feedId,
      uint32 interval,
      uint32 startTimestamp,
      int192[] calldata endPrices
  ) external onlyRole(EMERGENCY_CLOSE_ROUND_ROLE) whenPaused {
      if (endPrices.length == 0) revert
  ChainlinkUpDownAdapter__NoReportsToProcess();
      for (uint32 i = 0; i < endPrices.length; i++) {
          if (endPrices[i] <= 0) revert
  ChainlinkUpDownAdapter__EndPriceCannotBeZeroOrNegative();
          uint32 roundStartTimestamp = startTimestamp + i * interval;
          _closeRound(feedId, interval, roundStartTimestamp,
  endPrices[i]);
          emit ChainlinkUpDownAdapter__RoundEmergencyClosed(feedId,
  interval, roundStartTimestamp, endPrices[i]);
      }
  }
```

Also harden `_closeRound` to reject non-positive prices from both the emergency and CRE paths:

```solidity
  if (endPrice <= 0) revert
  ChainlinkUpDownAdapter__EndPriceCannotBeZeroOrNegative();
```

**Predict.fun:** Fixed in commit [478f88](https://github.com/PredictDotFun/prediction-market/commit/478f88cca369acaa28a1b334a6db873832c6b4de) & [6f0258](https://github.com/PredictDotFun/prediction-market/pull/71/commits/6f0258b2119675ef21588b909443c07e626127df).

**Cyfrin:** Verified.
