---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-0-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-09-cyfrin-firm-money-v2-0
title: Oracle fallback is inefficient and may choose price that is more stale
vuln_class: []
---

# Oracle fallback is inefficient and may choose price that is more stale

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-09-cyfrin-firm-money-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md)_

---

**Description:** `MainnetPriceFeedBase` rejects any Chainlink response older than `stalenessThreshold` and immediately falls back to `lastGoodPrice`.
However, `lastGoodPrice` has no associated timestamp, so the system cannot compare freshness between:
1. the rejected (slightly stale) oracle response, and
2. the stored `lastGoodPrice`.

As a result, the protocol can replace a newer but stale oracle value with an even older `lastGoodPrice`, worsening effective staleness.

**Impact:** Pricing during and after shutdown may rely on data older than the most recent oracle observation, increasing price distortion risk. Shutdown pricing may become less representative than necessary, even under available oracle data.

**Proof of Concept:** Assume:
- `stalenessThreshold = 24 hours`
- Current time = `T`
- Stored `lastGoodPrice = $2,000`, last updated at `T - 48h`
- Chainlink returns `answer = $1,800`, `updatedAt = T - 25h`

Execution:
1. `_isValidChainlinkPrice` checks `block.timestamp - updatedAt < stalenessThreshold` and returns `false` (`25h >= 24h`).
2. Feed is treated as failed and switches to `lastGoodPrice`.
3. Returned price becomes `$2,000` (48h old), instead of `$1,800` (25h old).

Result: fallback increased effective staleness by 23 hours and used a likely less accurate price.

**Recommended Mitigation:**
1. Store `lastGoodPriceTimestamp` whenever `lastGoodPrice` is updated.
2. On stale oracle path, compare recency of oracle response and lastGoodPriceTimestamp.

**Firm Money:**
Acknowledged. The situation could just as easily be that the oracle has been offline for months, like in the current case of the Mustang liquity fork. In which case we should deal with this by setting the debt limit to 0 or in other ways. The oracle price is a trusted limitation and if the oracle if offline for long periods of time we no longer trust it, so its a good assumption to go with the previous last good price that could be trusted.
Great find and nice edge case scenario though!
