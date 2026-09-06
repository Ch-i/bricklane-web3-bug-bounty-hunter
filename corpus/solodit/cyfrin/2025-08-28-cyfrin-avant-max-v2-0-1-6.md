---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-1-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Add an identifier or descriptor to `PriceStorage` which indicates what token
  or other entity is being priced
vuln_class: []
---

# Add an identifier or descriptor to `PriceStorage` which indicates what token or other entity is being priced

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** The `PriceStorage` contract contains no identifier or descriptor that would readily indicate what is being priced.

Consider adding an identifier or a descriptor such as a string that has the name of the token or entity being priced.

**Avant:**
Acknowledged: Avant will consider adding token identifiers in future `PriceStorage` deployments.

\clearpage
