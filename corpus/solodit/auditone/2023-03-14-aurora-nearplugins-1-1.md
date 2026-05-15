---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Lack of State Migration and State Integrality Check
vuln_class: []
---

# Lack of State Migration and State Integrality Check

_Section severity (from Solodit section header): Medium_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:**

In the current implementation, there is no state migration interface. In this case, the contract cannot deserialize the account's state due to the newly added attribute counter2.

**Recommendations:**

To fix the problem, users need to implement a method that migrates the old state, add the counter2 to the Counter. In order to check if the migration is correct, it's highly recommended to invoke a view function to get the whole contract state after the migration is completed. Add a migration interface for user
