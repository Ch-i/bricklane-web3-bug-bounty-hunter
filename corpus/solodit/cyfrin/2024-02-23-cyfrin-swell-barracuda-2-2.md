---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Missing events in `NodeOperatorRegistry` update methods
vuln_class: []
---

# Missing events in `NodeOperatorRegistry` update methods

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** The following functions in `NodeOperatorRegistry` update multiple storage locations but don't emit any events:
* `updateOperatorControllingAddress`
* `updateOperatorRewardAddress`
* `updateOperatorName`

Consider emitting events in these functions to reflect the updates made to storage.

**Swell:** Fixed in commit [5849640](https://github.com/SwellNetwork/v3-contracts-lst/commit/584964072b1543128c02e3287fe7746a8a094226).

**Cyfrin:**
Verified.
