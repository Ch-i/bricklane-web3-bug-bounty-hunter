---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Full access key is not removed on ownership change
vuln_class: []
---

# Full access key is not removed on ownership change

_Section severity (from Solodit section header): High_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** The full access key is not removed on changing owner. This allow old owner to still have ownership using the access key set by him.

- Owner Asets a new full access key using attach\_full\_access\_key function
- Owner is changed to Owner B
- Owner A still has control over the contract using the full access key (since the public key from step 1 is not removed, owner A still can use the access key to perform critical operations)

**Recommendations:**

- Tie access key with the owner who has set it. In case owner has changed that access key becomes useless

- Remove the access key on changing owner
