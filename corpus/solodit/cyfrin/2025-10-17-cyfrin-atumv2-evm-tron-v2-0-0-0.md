---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-17-cyfrin-atumv2-evm-tron-v2-0-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-10-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-17-cyfrin-atumv2-evm-tron-v2-0
title: Batch functions should revert on empty arrays
vuln_class: []
---

# Batch functions should revert on empty arrays

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md)_

---

**Description:** The newly added batch functions `Escrow::depositMany, releaseMany, refundMany` and `FulfillmentProxy::fulfillMany` should revert when their input arrays are empty; the current implementations will emit empty non-sensical events.

**Atum:**
Acknowledged; prefer lower gas costs by not including empty array checks.
