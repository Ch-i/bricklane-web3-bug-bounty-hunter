---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Emit missing events
vuln_class: []
---

# Emit missing events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** Emit missing events:
* `RequestsManager::constructor` should emit `AllowedTokenAdded`

**Avant:**
Fixed in commit [7a3587c](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/7a3587ca6d673d143565703d094b6f9526fd8020).

**Cyfrin:** Verified.
