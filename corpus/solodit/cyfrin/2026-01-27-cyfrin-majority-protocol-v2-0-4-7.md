---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Array length checks in `FixedRanksReward::getRewards`, `getReward` check against
  the wrong comparator
vuln_class: []
---

# Array length checks in `FixedRanksReward::getRewards`, `getReward` check against the wrong comparator

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** The check in `FixedRanksReward::getRewards` should compare using `>=` against input `winners.length`:
```diff
-        require(rankedRewards[sessionId].length > 0, RankedRewardsNotSet(sessionId));
+        require(rankedRewards[sessionId].length >= winners.length, RankedRewardsNotSet(sessionId));
```

Similarly the check in `FixedRanksReward::getReward` should compare using `>` against input `position`:
```diff
-       require(rankedRewards[sessionId].length > 0, RankedRewardsNotSet(sessionId));
+       require(rankedRewards[sessionId].length > position, RankedRewardsNotSet(sessionId));
```

The error should likely be changed to `PositionNotInRankedRewards` or something similar.

**Majority Games:**
Fixed in commit [6717163](https://github.com/Engage-Protocol/engage-protocol/commit/6717163d9d0fbe98a8c2af006b00da9edc20796f).

**Cyfrin:** Verified.
