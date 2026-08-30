---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: 'Subscribed message may get lost Severity: Medium'
vuln_class: []
---

# Subscribed message may get lost Severity: Medium

_Section severity (from Solodit section header): Medium_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

The subscribe function will stop if there is any error while sending the pubsub\_msg.


Restarting the subscribe function may take time

Within that time all published events would get lost and wont be processed.

**Recommendations:**

Probably an offchain component can keep track of all lost event messages and Admin could send those lost event messages so that they could be processed

Status: Resolved
