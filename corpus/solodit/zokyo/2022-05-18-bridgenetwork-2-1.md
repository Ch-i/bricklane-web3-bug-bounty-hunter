---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-05-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md
tags:
- firm:zokyo
- report:2022-05-18-bridgenetwork
title: In contract settings.sol there’s an assembly block at lines 62-64. This also
  applies to the bridge.sol file where there’s the same assembly block inside the
  constructor.
vuln_class: []
---

# In contract settings.sol there’s an assembly block at lines 62-64. This also applies to the bridge.sol file where there’s the same assembly block inside the constructor.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Extract the assembly block in a separate method and add a disable comment for the no-inline-
assembly warning. This way you don’t mix assembly methods with the code logic.
