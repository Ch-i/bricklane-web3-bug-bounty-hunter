---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-4-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Unnecessary `onlyRegisteredOperatorNode` on `completeStakeUpdate` function
vuln_class: []
---

# Unnecessary `onlyRegisteredOperatorNode` on `completeStakeUpdate` function

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** `completeStakeUpdate` is calling internal function `_completeStakeUpdate` which has the same modifier applied. Currently the modifier `onlyRegisteredOperatorNode` is checked twice.


**Recommended Mitigation:** Consider removing `onlyRegisteredOperatorNode` on `_completeStakeUpdate`

**Suzaku:**
Fixed in commit [f9946ef](https://github.com/suzaku-network/suzaku-core/commit/f9946ef8f6c7d7ab946e01d906f411352004ee41).

**Cyfrin:** Verified.
