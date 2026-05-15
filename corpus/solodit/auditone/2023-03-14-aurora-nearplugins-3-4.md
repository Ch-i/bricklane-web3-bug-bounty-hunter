---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-3-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Replace default panic with near-sdk panic
vuln_class: []
---

# Replace default panic with near-sdk panic

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:**

Currently, the codebase uses the default panic function to handle exceptional cases. This can lead to unexpected behavior and make it dicult to debug issues

**Recommendations:**

To improve the reliability and stability of the application, it is recommended to replace the default panic function with the panic function provided by the near-sdk. This panic function allows for more control over the handling of exceptional cases and can make it easier to debug and recover from issues.

Implementing this change will require updating all instances of the default panic function with the near\_sdk::panic function. It may also require updating any code that handles recovery from exceptional cases.
