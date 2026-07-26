---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-3-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: 'Unnecessary Initialization verification Severity: Quality Assurance'
vuln_class: []
---

# Unnecessary Initialization verification Severity: Quality Assurance

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**
The require! statement in the new function is used to check if the contract has already been initialized before. However, the function also uses the init macro which is responsible for initializing the contract. Since the init macro can only be called once per contract, there is no need for an additional check using require! to verify whether the contract has been initialized before.

**Recommendations:**

It is recommended to remove the unnecessary require! statement to ensure a cleaner and more efficient codebase.
