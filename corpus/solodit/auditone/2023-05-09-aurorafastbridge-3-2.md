---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-3-2
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
title: Improve handling of CheckToken case in check\_whitelist\_token\_and\_account
  function
vuln_class: []
---

# Improve handling of CheckToken case in check\_whitelist\_token\_and\_account function

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

In the check\_whitelist\_token\_and\_account function, the CheckToken variant of the WhitelistMode enum has an empty block, which might be unclear to readers of the code. This variant is intended to indicate that only the token needs to be checked against the whitelist, and no action is required for the associated account. However, the current implementation with an empty block might not effectively communicate this intent.

**Recommendations:**

 To improve the clarity and maintainability of the code, we recommend using the => {} pattern in the match statement for the CheckToken variant. This pattern makes it explicit that no action is needed for this case. Alternatively, you can add a comment within the empty block to explain why no action is required. Here's the updated match statement:
