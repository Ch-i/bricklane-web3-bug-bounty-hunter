---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: Outdated Dependencies
vuln_class: []
---

# Outdated Dependencies

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

The codebase is using an outdated Open Zeppelin version "@openzeppelin/contracts": "^4.2.0". Below are issues tied to outdated OZ versions. This lists errors such as DOS, improper initialization, etc.

**Recommendation**

Update Open Zeppelin dependencies to a more recent and secure version.

**Re-audit comment**

Resolved
