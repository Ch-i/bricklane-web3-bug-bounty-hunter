---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Remove obsolete `return` statements when using named return values
vuln_class: []
---

# Remove obsolete `return` statements when using named return values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Remove obsolete `return` statements when using named return values in:
* `DefaultSession::_calculatePlayerSessionResult`

**Majority Games:**
Fixed in commit [cc1c9d1](https://github.com/Engage-Protocol/engage-protocol/commit/cc1c9d17c69b817de2ff03e2b64ce5519a14df15).

**Cyfrin:** Verified.
