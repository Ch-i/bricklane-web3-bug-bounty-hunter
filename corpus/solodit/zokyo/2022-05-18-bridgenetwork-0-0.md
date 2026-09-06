---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-05-18T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md
tags:
- firm:zokyo
- report:2022-05-18-bridgenetwork
title: In contract "Controller", in function "addRegistrar", at lines 65 and 67, "validators.length"
  was used instead of "registrars.length".This leads to improper deletion of some
  values from the "registrars".
vuln_class: []
---

# In contract "Controller", in function "addRegistrar", at lines 65 and 67, "validators.length" was used instead of "registrars.length".This leads to improper deletion of some values from the "registrars".

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Through iteration from line 65, replace “validators.length” with “registrars.length”.
