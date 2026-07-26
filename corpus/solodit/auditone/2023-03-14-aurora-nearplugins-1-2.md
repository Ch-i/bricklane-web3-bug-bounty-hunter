---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Improper Full Access Key Fallback Design
vuln_class: []
---

# Improper Full Access Key Fallback Design

_Section severity (from Solodit section header): Medium_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

A Full Access Key could have total control over the account. It can transfer NEAR, deploy a smart contract and so on. Full access keys have more privileges than the owner and can do more things than the owner. In the current design, the owner of the contract can attach a new full-access key and can gain more privileges than expected.
