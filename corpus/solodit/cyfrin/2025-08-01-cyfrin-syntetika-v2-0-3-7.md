---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Emit missing event information
vuln_class: []
---

# Emit missing event information

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Emit missing event information:
* `YieldDistributed` should have the `timestamp` parameter in addition to the amount

**Syntetika:**
Fixed in commit [f4305a6](https://github.com/SyntetikaLabs/monorepo/commit/f4305a630d731455477a9979a9bb9bbdba541f00).

**Cyfrin:** Verified.
