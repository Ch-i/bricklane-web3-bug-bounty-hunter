---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Implement a reasonable hard-coded limit on maximum fees
vuln_class: []
---

# Implement a reasonable hard-coded limit on maximum fees

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Implement a reasonable hard-coded limit on maximum fees:
* `PublicBridge, PrivateChainBridge::constructor, setReleaseFee, setBridgeFee`

At the moment the contract owner could change the release fee to something unreasonable which would prevent users from releasing their tokens.

**BridgeX:**
Acknowledged; may implement in a future version.
