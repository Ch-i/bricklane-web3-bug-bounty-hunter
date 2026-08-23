---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Allow users to increment their nonce to void their signatures
vuln_class: []
---

# Allow users to increment their nonce to void their signatures

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** Currently users are unable to void their signatures by incrementing their nonce, since `NoncesUpgradeable::_useNonce` is `internal` and only called during actions which verify user signatures.

A user may want to invalidate a previous signature to prevent it from being used but is unable to.

**Impact:** Users are unable to invalidate previous signatures before they are used.

**Recommended Mitigation:** Expose `NoncesUpgradeable::_useNonce` via a `public` function that allows users to increment their own nonce.

**CryptoArt:**
Fixed in commit [cf82aeb](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/cf82aeb30d6a262cde51897f52c302be995d0202).

**Cyfrin:** Verified.
