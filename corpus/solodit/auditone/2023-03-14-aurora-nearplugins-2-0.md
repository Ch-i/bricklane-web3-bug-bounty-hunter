---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: No way to remove access key
vuln_class: []
---

# No way to remove access key

_Section severity (from Solodit section header): Low_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

Plugin has no way to remove an added access key

**Recommendations:** 

Add a new plugin method (owner only) which allows to remove an access key for given account
