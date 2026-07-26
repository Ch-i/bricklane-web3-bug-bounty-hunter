---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Unchecked Removal of the Paused\_Key
vuln_class: []
---

# Unchecked Removal of the Paused\_Key

_Section severity (from Solodit section header): Low_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

The function pa\_unpause\_feature() lacs a check on key's removal. The existence of the key is not checked. In this case, if the key does not exist, the contract will not panic, which may mislead the project manager and bring unexpected impacts.

**Recommendations:** 

Check the return value and panic if it is false.

**Status:** Resolved
