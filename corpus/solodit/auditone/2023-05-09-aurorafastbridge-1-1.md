---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: 'Redis db connection issue - Relayer fund loss Severity: Medium'
vuln_class: []
---

# Redis db connection issue - Relayer fund loss Severity: Medium

_Section severity (from Solodit section header): Medium_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

User A use fast bridge to get token on ETH

Relayer executes the transaction on ETH but due to redis issue, the PENDING\_TRANSACTIONS entry could not be made in Redis

This causes Relayer to be unaware about this issue and Relayer now wont issue lp\_unlock on near side

After bridge request expire user can unlock the token. This means user gets both token on eth and near side

**Recommendations:**

 Revert if redis connection issue is present Status: Resolved.
