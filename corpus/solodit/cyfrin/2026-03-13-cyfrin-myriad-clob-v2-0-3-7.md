---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-7
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
title: Neg-risk events have no void/cancellation path
vuln_class: []
---

# Neg-risk events have no void/cancellation path

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** Standalone binary markets support cancellation via `adminVoidMarket`, which sets `resolvedOutcome = -1`, records admin-specified payout ratios in `voidedPayouts`, and allows participants to recover collateral pro-rata through `ConditionalTokens::redeemVoided`.

Neg-risk event markets have no equivalent path. `adminVoidMarket` hard-blocks neg-risk markets:

```solidity
// PredictionMarketV3ManagerCLOB.sol:219
require(!market.negRisk, "use resolveEvent for neg risk");
```

And `NegRiskAdapter::resolveEvent` only accepts a winning outcome (`winningIndex >= -1`), where `-1` is explicitly the "Other" outcome, meaning no named candidate won, not a cancellation. If an event needs to be cancelled (oracle becomes unavailable, question is invalidated, regulatory action), the admin has no safe option:

- **Leave unresolved** - all participant collateral remains locked in `ConditionalTokens` indefinitely with no redemption path.
- **Resolve as "Other" wins** - all participant collateral is recovered by the adapter via its NO token redemptions and forwarded to treasury, rather than being refunded to participants.

Neither option is a fair cancellation.

**Recommended Mitigation:** Add a `voidEvent` function to `NegRiskAdapter` that calls `adminVoidMarket` on each underlying market with a provided payout split, sets `evt.resolved = true`, and handles the adapter's minted wcol accounting for the partial recovery scenario. This gives participants access to `redeemVoided` and recovers their collateral proportionally.

**Myriad:** Fixed in commit [`185c204`](https://github.com/Polkamarkets/polkamarkets-js/commit/185c204e8bcacccaf26566c6d62ecdc22211f986)

**Cyfrin:** Verified.
