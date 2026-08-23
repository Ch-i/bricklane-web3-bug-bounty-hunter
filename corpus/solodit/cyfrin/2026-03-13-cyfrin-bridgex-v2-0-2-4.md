---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Prefix `private, internal` function names with `_` character
vuln_class: []
---

# Prefix `private, internal` function names with `_` character

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Prefix `private, internal` function names with `_` character:
* `Token::updateBalance`

**BridgeX:**
Fixed in commit [c2d98c6](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/c2d98c6df7abdb3d99105ddde6d8ae5d7ed77ada).

**Cyfrin:** Verified.
