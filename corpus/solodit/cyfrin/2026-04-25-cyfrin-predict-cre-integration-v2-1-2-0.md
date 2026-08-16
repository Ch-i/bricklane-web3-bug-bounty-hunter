---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`chainlinkReports[i].interval` is caller-controlled, not in the DON-signed
  payload'
vuln_class: []
---

# `chainlinkReports[i].interval` is caller-controlled, not in the DON-signed payload

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `ReportV3` (defined in `IChainlinkAdapter.sol:13-23`) contains `{feedId, validFromTimestamp, observationsTimestamp, nativeFee, linkFee, expiresAt, price, bid, ask}` — there is **no `interval` field**. `ChainlinkUpDownAdapter::_processReport` at `ChainlinkUpDownAdapter.sol:244-245` reads `interval = chainlinkReports[i].interval` from the OUTER `ChainlinkReport[]` wrapper (set by the caller / CRE / forwarder), then calls `_closeRound(report.feedId, interval, report.observationsTimestamp - interval, report.price)`. A malicious or mis-configured forwarder can pair a genuinely DON-signed ReportV3 with an attacker-chosen `interval`, routing a valid price to the wrong round.

`IChainlinkAdapter.sol:13-23` shows the ReportV3 struct with no `interval` field. `ChainlinkUpDownAdapter.sol:244-245` reads `interval` from the outer wrapper, not from a signed field.

**Impact:** When multiple intervals are active on the same feedId and the alternative startTimestamp is also current (e.g. both `ts % 900 == 0 && ts % 300 == 0`), outcome steering becomes possible. Otherwise the mismatched route reverts via `NotCurrentRound`, limiting likelihood to Medium.

**Recommended Mitigation:** Either (a) move `interval` into the DON-signed payload so it cannot be tampered with, or (b) add a local consistency check: derive the interval from the target round config and require the caller-supplied value to match. Simplest local fix: ignore `chainlinkReports[i].interval` entirely and instead look up the active `(feedId, interval)` pair for which `observationsTimestamp - interval == currentRoundStartTimestamp` — resolve interval from adapter state, not from caller input.

**Predict.fun:** Acknowledged, this will revert since it can not match with any round config and the current round start timestamp.
