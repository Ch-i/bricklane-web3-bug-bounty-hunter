---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Pausable contract management should be handled by AccessControl plugin instead
  of the owner.
vuln_class: []
---

# Pausable contract management should be handled by AccessControl plugin instead of the owner.

_Section severity (from Solodit section header): Medium_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

In the current implementation, only the owner of the Pausable contract has the ability to pause or unpause it. This creates a potential security vulnerability, as the contract cannot be paused or unpaused if the owner's account is compromised or otherwise

unavailable. It also lacks accountability and transparency, as it may be dicult for other stakeholders to understand why certain actions were taken and whether they were justified. 

**Recommendations:**

- Update the Pausable contract to be managed by the AccessControl plugin instead of the owner.
- Implement additional security measures to protect the AccessControl plugin and ensure its availability.
- Ensure that all actions taken with the Pausable contract are properly documented and transparent to all stakeholders.
