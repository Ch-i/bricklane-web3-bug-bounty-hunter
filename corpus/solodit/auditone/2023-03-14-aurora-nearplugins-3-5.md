---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-3-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: revoke\_super\_admin\_unchecked not exposed through near bindgen
vuln_class: []
---

# revoke\_super\_admin\_unchecked not exposed through near bindgen

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

It has been reported that the revoke\_super\_admin\_unchecked function is not exposed through the near bindgen, preventing it from being accessed from external interfaces. 

**Recommendations:**

To ensure that the revoke\_super\_admin\_unchecked function can be used as intended, it is recommended to expose it through the near bindgen. This will allow the function to be accessed from external interfaces and used to revoke super administrative privileges as needed. It may also be helpful to implement safeguards to prevent accidental or malicious revocation of super administrative privileges.
