---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-22
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: In contract BaseToken, gov address has too much power and controls most critical  functions
  such as setting handler, adding and removing admins, toggling private mode, and
  setting token info.
vuln_class: []
---

# In contract BaseToken, gov address has too much power and controls most critical  functions such as setting handler, adding and removing admins, toggling private mode, and setting token info.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**  : Low

**Status**: Unresolved

**Recommendation**:

It is recommended that the gov address be a multisig address to prevent any single person acting maliciously at the expense of other participants.  

**Comment**: it's Partially fixed as side note below description and acknowledged as status since the client answer that this mechanism was implemented by design
