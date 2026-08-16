---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-2-6
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
title: Most of the .sol files in the contract directory are lower case, so are the
  names of the contracts. It’s preferred that contract names start with capital letters
  and follow a camelCase style.
vuln_class: []
---

# Most of the .sol files in the contract directory are lower case, so are the names of the contracts. It’s preferred that contract names start with capital letters and follow a camelCase style.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Refactor the contract names and if you wish also rename the .sol files to match the contract
casing. Also most of the code is not formatted correctly or using inconsistent indentation. Use
a tool such as solhint and format/indent the code correctly as it’s hard to follow. Also, for
further details check: https://docs.soliditylang.org/en/v0.8.11/style-guide.html
