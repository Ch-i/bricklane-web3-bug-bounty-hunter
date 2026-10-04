---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-7
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`deploy-full.ts` blindly retries one-shot deployment operations'
vuln_class: []
---

# `deploy-full.ts` blindly retries one-shot deployment operations

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** The deployment script uses `retry()` to resubmit a transaction after any error, including errors returned while waiting for the receipt. Some one-shot operations have read guards, but those guards are evaluated before entering `retry()` rather than on every attempt.

If the original transaction is mined successfully but receipt retrieval fails, the next attempt repeats the already-completed operation. One-shot calls such as `setRegistry`, `setTrust`, `setServiceConsumer`, `setPolicyId`, and `setRole` then revert instead of recognizing that their postcondition has already been satisfied.

Retried createPolicy may also create an unused additional policy.

**Impact:** A transient RPC or receipt-retrieval failure can cause deployment to abort after some operations have completed successfully. This may leave a partially handed-off stack requiring manual intervention or redeployment and may create unused contracts or policies.

**Recommended Mitigation:** Evaluate each operation’s postcondition inside the retry callback. After broadcasting a transaction, preserve its hash and attempt to recover its receipt before submitting another transaction.

**Securitize:** Acknowledged.
