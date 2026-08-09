---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Use input parameter when emitting events instead of reading `storage` when
  value already known
vuln_class: []
---

# Use input parameter when emitting events instead of reading `storage` when value already known

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Use input parameter when emitting events instead of reading storage when value already known:
* `Token::transferOwnership` - `emit TransferOwnership(newOwner, false);`
* `Token::setIssuer` - `emit NewIssuer(newIssuer);`

**BridgeX:**
Fixed in commit [a372b10](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/a372b106f6fbc91d051df37f05ad0e46ff648751).

**Cyfrin:** Verified.

\clearpage
