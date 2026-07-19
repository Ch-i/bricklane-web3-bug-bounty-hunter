---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-4-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Redundant overflow checks in safe arithmetic operations
vuln_class: []
---

# Redundant overflow checks in safe arithmetic operations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** `Solidity 0.8.25` includes built-in overflow checks for arithmetic operations, which add ~20-30 gas per operation. In `UptimeTracker::computeValidatorUptime`, operations like loop increments (i++) and additions (lastUptimeEpoch + i) are guaranteed not to overflow due to the use of uint48 and controlled inputs.

**Recommended Mitigation:** Use unchecked blocks for safe arithmetic operations:
```solidity

for (uint48 i = 0; i < elapsedEpochs;) {
    uint48 epoch;
    unchecked {
        epoch = lastUptimeEpoch + i;
        i++;
    }
    // ...
}
```

**Suzaku:**
Fixed in commit [2fb0daf](https://github.com/suzaku-network/suzaku-core/commit/2fb0dafd684eeaf11b177602c5047d1e6ce2d715).

**Cyfrin:** Verified.

\clearpage
