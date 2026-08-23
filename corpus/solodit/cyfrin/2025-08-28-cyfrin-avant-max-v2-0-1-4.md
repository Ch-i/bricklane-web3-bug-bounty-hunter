---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Add `deadline` parameter for mint and burn requests in `RequestsManager`
vuln_class: []
---

# Add `deadline` parameter for mint and burn requests in `RequestsManager`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** `RequestsManager::requestMint` and `requestBurn` allow callers to specify the minimum output amount but don't allow callers to specify a deadline for the request to be completed.

Minimum output amounts become "stale" over time; what users would expect as the minimum today could be different tomorrow and different again next week.

It would be ideal to allow callers of `RequestsManager::requestMint` and `requestBurn` to specify a deadline by which the requests must be completed. Past the deadline completion should revert but cancellation must remain possible.

**Avant:**
Considering users can cancel mint and burn requests at any time, and they have already specified their minimum expected output amount, we believe the suggested extra constraint might not add much value while increasing the complexity of the UX.
