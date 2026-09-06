---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: No way for users to invalidate nonce used to sign
vuln_class: []
---

# No way for users to invalidate nonce used to sign

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** After signing a transaction, users may change their mind and wish to invalidate their signature. In this case users should have a function to call that invalidates their nonce.

In places such as `SecuritizeSwap::executePreApprovedTransaction`, there is no function which allows users to increase (and thereby invalidate) their current nonce.

**Impact:** Users are unable to revoke a signature before it has been used as they can't invalidate their current nonce.

**Recommended Mitigation:** Create a function that users can call which just increments their current nonce. Also check `MultiSigWallet`, `TransactionRelayer` and other places using signatures.

**Securitize:** Acknowledged.
