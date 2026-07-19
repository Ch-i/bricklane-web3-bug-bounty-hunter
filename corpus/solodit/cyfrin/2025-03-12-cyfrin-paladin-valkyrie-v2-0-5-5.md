---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-5-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Superfluous assignment can be removed
vuln_class: []
---

# Superfluous assignment can be removed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** The assignment of `newDuration` to `maxDuration` within `TimeWeightedIncentiveLogic::_earnedTimeWeigthed` when it exceeds this value can be removed as this case is handled in the subsequent conditional block and so is effectively a no-op.

**Recommended Mitigation:**
```diff
--  if (newDuration >= maxDuration) newDuration = maxDuration;
    uint256 ratio;
    if (newDuration >= maxDuration) {
        uint256 remainingIncreaseDuration = maxDuration - _checkpoint.duration;
        uint256 left = ((((maxDuration - _checkpoint.duration - 1) * UNIT) / 2) / maxDuration);
        ratio =
            ((left * remainingIncreaseDuration) + (UNIT * (timeDiff - remainingIncreaseDuration))) / timeDiff;
    } else {
        ratio = ((((newDuration - _checkpoint.duration - 1) * UNIT) / 2) / maxDuration);
    }
```

**Paladin:** Fixed by commit [`f8dc21e`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/f8dc21e765f6b2568ae221dc5e2855181896c6bb).

**Cyfrin:** Verified. The assignment has been removed.

\clearpage
