---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-0-3
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
title: 'Malicious user can double-unlock his locked funds Severity: High'
vuln_class: []
---

# Malicious user can double-unlock his locked funds Severity: High

_Section severity (from Solodit section header): High_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

Currently unlock function checks whether pending transfer of the nonce does exist or not, after its success, the callback function increases balance and remove transfer.

In Near, main call and callback handler are independent transaction, so a malicious user can call unlock repeatedly, before callback function finished.

As pending transfer is not removed yet, user can still pass the check in second call.

Second call of remove\_transfer in callback will not panic but only return None.

As a result, user can double-unlock his funds.

**Recommendations:**

We should check if the nonce still exists in the pending\_transfers at unlock\_callback.
