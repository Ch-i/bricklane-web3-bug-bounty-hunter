---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Timelock behind up\_deploy\_code
vuln_class: []
---

# Timelock behind up\_deploy\_code

_Section severity (from Solodit section header): Medium_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:**User should get considerable time to opt out of an upgraded code. Since up\_deploy\_code does not require any delay, a malicious owner can simply deploy malicious code instantly.

- An innocent contract Ais deployed with high staking APR
- User starts investing using the contract
- Owner stages and deploys a malicious code which adds a new function to drain user funds
- User funds get stolen

**Recommendations:** Place up\_deploy\_code function behind timelock which gives user suitable time to make decision
