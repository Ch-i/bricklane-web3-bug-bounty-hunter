---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-05-18-bridgenetwork-2-5
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
title: There is mixed usage of error messages when reverted inside functions. Some
  error messages are incomplete or plain abbreviations that are explained inside errorsMsgs.txt.
  That’s not the preferred way to have error messages.
vuln_class: []
---

# There is mixed usage of error messages when reverted inside functions. Some error messages are incomplete or plain abbreviations that are explained inside errorsMsgs.txt. That’s not the preferred way to have error messages.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-05-18-BridgeNetwork.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-05-18-BridgeNetwork.md)_

---

**Recommendation**:

Remove the .txt file and add full length error messages whenever there’s require.
