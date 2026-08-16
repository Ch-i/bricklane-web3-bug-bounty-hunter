---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Emit missing events for important state changes
vuln_class: []
---

# Emit missing events for important state changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Emit missing events for important state changes:
* `PublicBridge, PrivateChainBridge::addReleaser, removeReleaser, setRequiredSignatures, setChainId`

**BridgeX:**
Fixed in commit [5899b57](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/5899b573f7c4f57aa27b358b3f3c9932a1699db5).

**Cyfrin:** Verified.
