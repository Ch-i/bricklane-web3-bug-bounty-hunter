---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-0-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`enableRoundConfig` uses `<=` instead of `<`, forcing an unnecessary one-interval
  gap when re-enabling a round series'
vuln_class: []
---

# `enableRoundConfig` uses `<=` instead of `<`, forcing an unnecessary one-interval gap when re-enabling a round series

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `enableRoundConfig` is called by the admin to restart a round series after it has been disabled. It validates that the new series does not overlap with the previous one by checking that `newCurrentRoundStartTimestamp` is past the end of the previous series' last round:

```solidity
        if (newCurrentRoundStartTimestamp <= roundConfig.latestRoundStartTimestamp + interval) {
            revert ChainlinkUpDownAdapter__NewCurrentRoundStartTimestampMustBeGreaterThanLatestRoundEndTimestamp();
        }
```

The expression `latestRoundStartTimestamp + interval` is the end timestamp of the last round in the previous series — as confirmed by the revert error name itself (...`GreaterThanLatestRoundEndTimestamp`). Using ` <=`  means that starting at exactly that boundary is rejected, even though the previous round has already fully ended at that timestamp.

Because `newCurrentRoundStartTimestamp` must also be divisible by interval, the smallest valid timestamp after the `<=` rejection is `latestRoundStartTimestamp + 2 * interval` — one full interval beyond the natural restart point.

We can also see that when rounds are created they start exactly at `latestRoundStartTimestamp + interval`

```solidity
if (roundConfig.isEnabled) {
            uint32 newLatestTimestamp = roundConfig.latestRoundStartTimestamp + interval;
            roundConfig.latestRoundStartTimestamp = newLatestTimestamp;
            _createRound(feedId, newLatestTimestamp, interval);
        }
```

**Impact:** Admins cannot re-enable a round series at the natural boundary immediately following the last round's end. The earliest valid restart is always at least one full interval later than expected. For long intervals (e.g. 1 hour, 4 hours, 1 day), this creates a mandatory dead period during which no market exists for that feed, directly harming continuity of the prediction market and user experience. A gap of one interval with no active market means no trading, no liquidity, and potential loss of user engagement for a predictable and avoidable window.

**Proof of Concept:** **Setup**:

- `interval` = 900 (15 minutes)
- `latestRoundStartTimestamp` = 54000 (15:00)
- Last round ends at: 54000 + 900 = 54900 (15:15)
- Admin calls `enableRoundConfig` with `newCurrentRoundStartTimestamp`= 54900 (15:15 — the exact natural restart point):

54900 <= 54900  →  TRUE  →  REVERT

**Recommended Mitigation:** Change <= to < so that the admin can restart the series at exactly the natural boundary.

**Predict.fun:** Fixed in commit [98569bc](https://github.com/PredictDotFun/prediction-market/pull/71/changes/98569bcbab3177d0e84010159e7e1dcd2d9ab36f).

**Cyfrin:** Verified.

\clearpage
