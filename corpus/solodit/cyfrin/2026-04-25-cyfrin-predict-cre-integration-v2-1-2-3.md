---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Event emission gaps and telemetry asymmetries
vuln_class: []
---

# Event emission gaps and telemetry asymmetries

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `ChainlinkUpDownAdapter::_closeRound` normal path emits no close event — only `emergencyCloseRounds` does. `RoundStartPriceSet` emits the recorded (possibly stale — see the H-1 issue) price rather than the supplied one. Off-chain reconstruction harder.

**Impact:** Off-chain indexers and monitoring lose visibility into normal-path closures and may log misleading start-price values.

**Recommended Mitigation:** Emit `ChainlinkUpDownAdapter__RoundClosed(feedId, interval, startTimestamp, endPrice, outcome)` at the tail of `_closeRound`. Fix `RoundStartPriceSet` to emit the supplied `startPrice` (see the H-1 issue's mitigation).

**Predict.fun:** Acknowledged, they conclude that having the `RoundStartPriceSet` event is good enough.
