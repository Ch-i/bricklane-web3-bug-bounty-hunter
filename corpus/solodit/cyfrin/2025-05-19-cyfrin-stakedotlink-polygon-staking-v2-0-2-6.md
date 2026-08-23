---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-2-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Missing input validation in `PolygonFundFlowController.setMinTimeBetweenUnbonding`
vuln_class: []
---

# Missing input validation in `PolygonFundFlowController.setMinTimeBetweenUnbonding`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** The `setMinTimeBetweenUnbonding` function from `PolygonFundFlowController` lacks input validation for the `_minTimeBetweenUnbonding` parameter, allowing it to be set to any value including zero or extremely high values.
```solidity
    function setMinTimeBetweenUnbonding(uint64 _minTimeBetweenUnbonding) external onlyOwner {
        minTimeBetweenUnbonding = _minTimeBetweenUnbonding;  // @audit missing input validation
        emit SetMinTimeBetweenUnbonding(_minTimeBetweenUnbonding);
    }
```

**Recommended Mitigation:** Add a min/max value check before setting the `minTimeBetweenUnbonding`. I.e:
```diff
// declare MIN_VALUE and MAX_VALUE with the proper values.
function setMinTimeBetweenUnbonding(uint64 _minTimeBetweenUnbonding) external onlyOwner {
+    require(_minTimeBetweenUnbonding >= MIN_VALUE, "Time between unbonding too low");
+    require(_minTimeBetweenUnbonding <= MAX_VALUE, "Time between unbonding too high");

    minTimeBetweenUnbonding = _minTimeBetweenUnbonding;
    emit SetMinTimeBetweenUnbonding(_minTimeBetweenUnbonding);
}
```

**Stake.Link:** Acknowledged. Owner will ensure correct value is set.

**Cyfrin:** Acknowledged.
