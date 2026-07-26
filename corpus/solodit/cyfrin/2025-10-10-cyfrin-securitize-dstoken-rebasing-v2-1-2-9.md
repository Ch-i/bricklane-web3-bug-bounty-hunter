---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: No deadline for user signatures
vuln_class: []
---

# No deadline for user signatures

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Signatures signed by users should always have an [expiration or timestamp deadline](https://dacian.me/signature-replay-attacks#heading-no-expiration), such that after that time the signature is no longer valid.

When users sign a transaction they should sign using a future expiry deadline and the function processing that signature should revert if the deadline has elapsed.

**Recommended Mitigation:** Functions such as `SecuritizeSwap::executePreApprovedTransaction` should take a user-supplied deadline as input, and `doExecuteByInvestor` should revert if it has expired otherwise include it when calculating the hash along with the other parameters. Also check `MultiSigWallet`, `TransactionRelayer` and other places using signatures.

Could also consider adding a deadline to functions such as `SecuritizeSwap::buy` even if they don't use a signature, though since that function has a slippage parameter the benefit is not as great.

**Securitize:** Most of the affected contracts were deleted as they were obsolete, the only one that remains is `TransactionRelayer` which we'll leave as is.

**Cyfrin:** Verified.
