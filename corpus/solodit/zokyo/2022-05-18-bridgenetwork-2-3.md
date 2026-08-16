---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-2-3
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
title: There are multiple versions of solidity in different files. For example in
  tokenLock.sol the version declared is pragma solidity ^0.8.2,but the declared compiler
  version in hardhat.config is 0.8.0.
vuln_class: []
---

# There are multiple versions of solidity in different files. For example in tokenLock.sol the version declared is pragma solidity ^0.8.2,but the declared compiler version in hardhat.config is 0.8.0.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Use consistent versioning.
