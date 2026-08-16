---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-05-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md
tags:
- firm:zokyo
- report:2022-05-18-bridgenetwork
title: When running the coverage tool with the solidity optimizer disabled it results
  in a stack too deep error when compiling. This happens because the EVM is limited
  to assigning 16 slots for local variables. Running with optimizer solves the is
vuln_class: []
---

# When running the coverage tool with the solidity optimizer disabled it results in a stack too deep error when compiling. This happens because the EVM is limited to assigning 16 slots for local variables. Running with optimizer solves the issue but most of the external plugins, like solidity-coverage, does not support the optimizer, to have better access to tolling and plugins we will recommend to fix the issue.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

![image](https://github.com/user-attachments/assets/48fa4873-3dd9-4b37-b5c7-d354eac6a064)

**Recommendation**:

Refactor functions that have many local variables and try to split them in smaller and more
manageable functions.
