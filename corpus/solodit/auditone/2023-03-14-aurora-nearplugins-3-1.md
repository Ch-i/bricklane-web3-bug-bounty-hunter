---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Unnecessary Clone
vuln_class: []
---

# Unnecessary Clone

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

The functions return Vec<u8> so we need to copy the slice on the memory to construct a new Vec.

while 'static [u8]is a reference, there is no copy needed.

Thus, we can return 'static [u8]directly.

**Recommendations:** 

Change return type from Vec<u8> to 'static [u8]and remove to\_vec().
