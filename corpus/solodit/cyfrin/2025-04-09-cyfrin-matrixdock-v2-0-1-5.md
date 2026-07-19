---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Use consistent prefix for `internal` function names
vuln_class: []
---

# Use consistent prefix for `internal` function names

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** Some of the `internal` functions use a `_` prefix character but others don't. Use `_` as a consistent prefix for all `internal` function names:

* `MTokenMessager::sendDataToChain`
* `MTokenMessagerLZ::sendThroughLZ`
* `MTokenMessagerV2::sendDataToChain`

**Matrixdock:** Acknowledged.
