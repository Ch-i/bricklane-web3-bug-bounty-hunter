---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-3-2
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
title: Question about the design purpose of the Full Access Key Fallback
vuln_class: []
---

# Question about the design purpose of the Full Access Key Fallback

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

The comment says Smart contracts can be considered trustless, when there is no Full Access Key (FAK) attached to it. Otherwise owner of the FAKcan redeploy or use the funds stored on the smart contract.

However, according to the doc[umentation, remov](https://docs.near.org/concepts/basics/accounts/access-keys#locked-accounts)ing the contracts' FAKis suggested to make the contract fully de-centralized.
