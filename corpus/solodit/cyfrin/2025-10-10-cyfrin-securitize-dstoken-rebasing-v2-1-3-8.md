---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Prefer `ECDSA::tryRecover` to using `ecrecover` directly
vuln_class: []
---

# Prefer `ECDSA::tryRecover` to using `ecrecover` directly

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ecrecover` is susceptible to [signature malleability](https://dacian.me/signature-replay-attacks#heading-signature-malleability) so it is not recommended to use it directly.

Prefer [ECDSA::tryRecover](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol#L169-L174) in `MultiSigWallet` and `TransactionRelayer`.

**Securitize:** `TransactionRelayer` was significantly refactored and now uses OZ `ECDSA`. `MultiSigWallet` was removed as it was deprecated.

**Cyfrin:** Verified.
