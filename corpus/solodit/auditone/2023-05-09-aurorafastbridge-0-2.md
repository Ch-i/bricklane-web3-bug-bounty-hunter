---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-0-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: 'User can drain all funds by calling withdraw multiple times Severity: High'
vuln_class: []
---

# User can drain all funds by calling withdraw multiple times Severity: High

_Section severity (from Solodit section header): High_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

Currently withdraw function transfer tokens and after its success, the callback function decreases user's balance. As main call and callback handler are independent transaction, a malicious user can call withdraw repeatedly, before callback function called.

As user's balance is still not decreased, user can still transfer tokens.

**Recommendations:**

We should follow CEI pattern in this case.

We should move decrease\_balance to withdraw, above ft\_transfer.
