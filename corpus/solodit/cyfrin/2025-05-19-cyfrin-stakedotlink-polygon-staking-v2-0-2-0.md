---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Missing event emission for PolygonStrategy::setFundFlowController
vuln_class: []
---

# Missing event emission for PolygonStrategy::setFundFlowController

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** A crucial strategy parameter ie. the `fundFlowController` can be updated by the owner. However no event emission exists for such an update.

**Recommended Mitigation:** Consider emitting an event for the `setFundFlowController` function.

**Stake.Link:** Acknowledged. `fundFlowController` is only ever set once at time of contract deployment

**Cyfrin:** Acknowledged.
