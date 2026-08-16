---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-08-25-boba-network-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-08-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md
tags:
- firm:zokyo
- report:2022-08-25-boba-network
title: Config param sanity check for `_srcAddress` in LzApp forceResumeReceive.
vuln_class: []
---

# Config param sanity check for `_srcAddress` in LzApp forceResumeReceive.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-08-25-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md)_

---

**Description**

In contract LzApp.sol, in the function force Resume Receive, there's no sanity check for the _srcAddress parameter. This can generate a wrong assignment, even if the route can only be accessed by the owner of the contract.

**Recommendation**

Add a sanity check to prevent_srcAddress from being an empty slice of bytes.

**Re-audit comment**

Acknowledged
