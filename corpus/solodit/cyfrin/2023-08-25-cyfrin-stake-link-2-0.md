---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-08-25-cyfrin-stake-link-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md
tags:
- firm:cyfrin
- report:2023-08-25-cyfrin-stake-link
title: Unnecessary event emissions
vuln_class: []
---

# Unnecessary event emissions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-08-25-cyfrin-stake-link.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md)_

---

`PriorityPool::setPoolStatusClosed` does not check if pool status is already `CLOSED` and emits `SetPoolStatus` event. Avoid event emission if the pool status is already closed. Avoid this. The same applies to the function `setPoolStatus` as well.

**Client:**
Fixed in this [PR](https://github.com/stakedotlink/contracts/pull/32).

**Cyfrin:** Verified.
