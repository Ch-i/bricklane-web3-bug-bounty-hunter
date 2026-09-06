---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-2-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-05-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md
tags:
- firm:zokyo
- report:2022-05-18-bridgenetwork
title: In contract “Wrapped Deployer”, the variable “lossessEnabled” is initialized
  when it is declared at line 11 and there is no way to modify it.
vuln_class: []
---

# In contract “Wrapped Deployer”, the variable “lossessEnabled” is initialized when it is declared at line 11 and there is no way to modify it.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

The variable should be initialized through the constructor and a function should be added to
allow the variable to be modified.
