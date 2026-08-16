---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-2
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
title: Fix comment in `revealSolution`
vuln_class: []
---

# Fix comment in `revealSolution`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** The comment above `revealSolutions` says it is is meant to be called by the session manager but that's not true anymore, anyone can call it.

**Majority Games:**
Fixed in commit [acb42cb](https://github.com/Engage-Protocol/engage-protocol/commit/acb42cbc4422d6ade640864b4d74dd3beffbcebc).

**Cyfrin:** Verified.
