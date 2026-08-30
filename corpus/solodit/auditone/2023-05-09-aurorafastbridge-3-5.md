---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-3-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: Wrong parameter on lp\_unlock near call at unlock\_tokens in Relayer
vuln_class: []
---

# Wrong parameter on lp\_unlock near call at unlock\_tokens in Relayer

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

From Relayer, it passes { nonce, proof } as param to lp\_unlock call.

However, actual near implementation has just one param proof.![ref5]

**Recommendations:**

As proof includes nonce and everything looks good at Near side, we should keep consistency and remove nonce from lp\_unlock call from Relayer.
