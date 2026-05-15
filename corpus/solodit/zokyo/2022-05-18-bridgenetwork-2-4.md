---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-05-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md
tags:
- firm:zokyo
- report:2022-05-18-bridgenetwork
title: There are multiple contracts where global variables have no explicit visibility
  declarations. For example in the settings.sol file at line 17 there’s no visibility
  declared.
vuln_class: []
---

# There are multiple contracts where global variables have no explicit visibility declarations. For example in the settings.sol file at line 17 there’s no visibility declared.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Add explicit visibility declarations in all contracts and consider refactoring global variables in
groups, such as public and private groups.
