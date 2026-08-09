---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-7
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
title: Use `msg.sender` instead of `owner` inside `onlyOwner` functions
vuln_class: []
---

# Use `msg.sender` instead of `owner` inside `onlyOwner` functions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Use `msg.sender` instead of `owner` inside `onlyOwner` functions:
* `PublicBridge, PrivateChainBridge::transferOwnership`

**BridgeX:**
Fixed in commit [cb04abb](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/cb04abb3aa1cf82f24d500c9a8e8f8774ad8ce54).

**Cyfrin:** Verified.
