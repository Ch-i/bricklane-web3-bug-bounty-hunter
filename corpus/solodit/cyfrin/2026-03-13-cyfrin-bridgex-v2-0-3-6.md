---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Use input value instead of defining additional variable when original input
  value doesn't need to be preserved
vuln_class: []
---

# Use input value instead of defining additional variable when original input value doesn't need to be preserved

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Use input value instead of defining additional variable when original input value doesn't need to be preserved:
* `PublicBridge::lockTokens` - remove `bridgeAmount` and just use/modify `amount`

**BridgeX:**
Fixed in commit [521ff55](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/521ff55a00ef1d3aca64250371e903635fe7611e).

**Cyfrin:** Verified.
