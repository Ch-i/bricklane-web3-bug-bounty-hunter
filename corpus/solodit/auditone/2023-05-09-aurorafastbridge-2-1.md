---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: Lack of Check for Same token\_eth and recipient in the NEAR Contract
vuln_class: []
---

# Lack of Check for Same token\_eth and recipient in the NEAR Contract

_Section severity (from Solodit section header): Low_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:** 
In the provided code snippet, a JSON object is created, containing the details for a transfer, including the token\_eth and recipient fields. However, there is no check to ensure that the token\_eth and recipient fields are not the same. Allowing the same value for both fields could lead to potential issues in the contract's execution, as it might not be the intended behavior for a valid transfer.

**Recommendations:**

To address this issue, it is recommended that the NEAR contract includes a check to ensure that the token_eth and recipient fields are not the same.
