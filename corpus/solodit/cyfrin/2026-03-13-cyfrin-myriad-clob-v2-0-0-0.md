---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Oracle void outcome leaves `PredictionMarketV3ManagerCLOB.voidedPayouts` unset,
  locking collateral
vuln_class: []
---

# Oracle void outcome leaves `PredictionMarketV3ManagerCLOB.voidedPayouts` unset, locking collateral

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `PredictionMarketV3ManagerCLOB::resolveMarket` accepts `outcome == -1` from an oracle and marks the market as resolved with `resolvedOutcome = -1`, but it never populates `voidedPayouts[marketId]`.

```solidity
// PredictionMarketV3ManagerCLOB.sol:174-182
(int256 outcome, bool resolved) = IMarketOracle(market.oracle).getResult(marketId);
require(resolved, "oracle: not resolved");
require(outcome == 0 || outcome == 1 || outcome == -1, "invalid outcome");

market.resolvedOutcome = outcome;   // can be -1
market.state = MarketState.resolved;
// voidedPayouts[marketId] is never set — defaults to [0, 0]
```

This is not a theoretical edge case. The protocol intends to use [reality.eth](https://reality.eth.limo/app/docs/html/contracts.html#fetching-the-answer-to-a-particular-question) as its oracle. reality.eth encodes invalid or unanswered questions as `0xfff...fff`, which when cast to `int256` is exactly `-1`. This value is returned whenever a question is declared invalid by the arbitrator or times out without a valid answer, both are realistic market scenarios.

When token holders later call `ConditionalTokens::redeemVoided`, it fetches payouts from `getVoidedPayouts` and asserts they sum to `1e18`:

```solidity
// ConditionalTokens.sol:77-78
(uint256 outcome0Payout, uint256 outcome1Payout) = manager.getVoidedPayouts(marketId);
require(outcome0Payout + outcome1Payout == 1e18, "invalid payout ratios"); // 0 + 0 ≠ 1e18 → always reverts
```

The require will always fail for oracle-voided markets, making the collateral backing those outcome tokens unrecoverable.

**Impact:** All collateral deposited by position holders in oracle-voided markets is locked in `ConditionalTokens` with no immediate recovery path. Because `PredictionMarketV3ManagerCLOB` is UUPS upgradeable, the funds are not permanently lost, a patched implementation can be deployed to set the missing `voidedPayouts` and unblock redemptions. However, this requires a full development, audit, and deployment cycle, during which affected users cannot access their collateral.

**Recommended Mitigation:** Reject `outcome == -1` from the oracle in `resolveMarket`, forcing all voids through `adminVoidMarket` which correctly sets payout ratios:

```solidity
require(outcome == 0 || outcome == 1, "oracle: invalid outcome");
```

**Myriad:** Fixed in commit [`9169487`](https://github.com/Polkamarkets/polkamarkets-js/commit/91694876d3bad218a20d5e3474becfe8e482a610)

**Cyfrin:** Verfied. Oracle outcome `-1` now reverts.
