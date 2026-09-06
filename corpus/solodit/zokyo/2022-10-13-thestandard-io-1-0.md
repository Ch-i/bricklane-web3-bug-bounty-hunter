---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Duplicate token addition allowed in TokenManager.
vuln_class: []
---

# Duplicate token addition allowed in TokenManager.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

TokenManager.sol
addAccepted Token function allows the owner to add the same token multiple times

**Recommendation**

Allow only unique tokens to be added to the accepted token symbols.

**Re-audit comment**

Resolved
