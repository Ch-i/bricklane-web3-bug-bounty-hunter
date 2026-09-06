---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Condition addresses can re-enter `StrategyBuilderPlugin`
vuln_class: []
---

# Condition addresses can re-enter `StrategyBuilderPlugin`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** Condition addresses can re-enter `StrategyBuilderPlugin` from the external call in `_changeStrategyInCondition()` and similarly in `_changeAutomationInCondition()`. In the latter case, it seems that the worst thing that can happen here is duplicating the array entry when pushing to `strategiesUsed` which corrupts `automationsToIndex` and prevents the duplicate from being removed (unless there is re-entrancy during the deletion as well). Impact is therefore limited, but it is important to be aware of this when making any future modifications.

**OctoDeFi:** Acknowledged. We have taken note of the reentry issue.

**Cyfrin:** Acknowledged.

\clearpage
