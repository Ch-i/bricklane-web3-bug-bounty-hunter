---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: '`SpeedCalculator::calcSpeed` should return early if `_moduleBudget` is zero'
vuln_class: []
---

# `SpeedCalculator::calcSpeed` should return early if `_moduleBudget` is zero

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** `SpeedCalculator::calcSpeed` currently short circuits if any of the `_totalVotes`, `_epochDuration`, or `_votes` parameters are zero. This is beneficial as it avoids wasting gas on unnecessary computation; however, this validation should also include the `_moduleBudget` as multiplication by zero would similarly result in zero being returned.

**Recommended Mitigation:**
```diff
function calcSpeed(
    uint256 _votes,
    uint256 _totalVotes,
    uint256 _moduleBudget,
    uint256 _epochDuration
) public pure returns (uint256) {
-   if (_totalVotes == 0 || _epochDuration == 0 || _votes == 0) return 0;
+   if (_totalVotes == 0 || _epochDuration == 0 || _votes == 0 || _moduleBudget == 0) return 0;

    return
        (_moduleBudget * SPEED_PRECISION * _votes) /
        (_epochDuration * _totalVotes * SPEED_PRECISION);
}
```

**BENQI:** Fixed in PR [\#15](https://github.com/aragon/benqi-governance/pull/15).

**Cyfrin:** Verified.
