---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: Potential for Race Condition between Unlock Time and Proof Verification leading
  to Double Spending
vuln_class: []
---

# Potential for Race Condition between Unlock Time and Proof Verification leading to Double Spending

_Section severity (from Solodit section header): High_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:** 

In the Fast Bridge project, a race condition between unlock time and proof verification can lead to double spending. Here's how it can happen:

When a user sends tokens from Ethereum to NEAR, the tokens are locked on the Ethereum side, and the LP-Relayer is responsible for releasing the tokens on the NEAR side once the proof of transaction has been received. The LP-Relayer has a specific time window in which to release the tokens, which is set by the sender when they initiate the transaction.

**Recommendations:**

To prevent this from happening, it's important that the LP- Relayer is trusted and secure, and that there are appropriate measures in place to verify that the proof of transaction is valid before the tokens are released. This can include using secure verification processes, and having multiple parties involved in verifying the proof before the tokens are released.
