---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-3-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: 'Lack of Configurability for Timeouts in Fast Bridge Service Severity: Quality
  Assurance'
vuln_class: []
---

# Lack of Configurability for Timeouts in Fast Bridge Service Severity: Quality Assurance

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

The Fast Bridge project has a lack of configurability for timeouts related to transactions. In the code snippet provided, there is a hardcoded timeout of 60 seconds, which may not be sufficient for all transactions. This lack of configurability could result in delays or even failures of transactions, especially in cases where longer confirmation times are required.

**Recommendations:**

To address this issue, it is recommended ![ref5]that the Fast Bridge project implement a more configurable approach for timeouts related to transactions.

Status: Resolved.
