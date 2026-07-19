---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: Lack of Validation for valid\_till\_block\_height on FastBridge Service
vuln_class: []
---

# Lack of Validation for valid\_till\_block\_height on FastBridge Service

_Section severity (from Solodit section header): Medium_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:** 

The FastBridge Service, which is responsible for managing transfers between the NEAR and Ethereum networks, does not validate the valid\_till\_block\_height parameter. This parameter is used to set an expiration block height for the transfer, and if not validated properly, it could result in transfers being processed after they have expired.

**Recommendations:**

To address this issue, it is recommended that the ![ref4]FastBridge Service implement proper validation for the valid\_till\_block\_height parameter. This could include checks to ensure that the current block height is not greater than the valid\_till\_block\_height value.
