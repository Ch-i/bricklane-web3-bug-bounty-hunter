---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Optional `signature` field specified in legal agreement but not implemented
  in `Chain` struct
vuln_class: []
---

# Optional `signature` field specified in legal agreement but not implemented in `Chain` struct

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** The SEAL Whitehat Safe Harbor Agreement legal document specifies an optional `signature` field within the `Chain` struct that is not implemented in the smart contract code.

>Legal Agreement Reference (Section 1.1(c)(ii)):
"D. optionally, the signature for such account, which may be used as additional evidence that such account has affirmatively accepted being subject to this Agreement."

This field was designed to allow protocols to provide cryptographic proof that specific accounts on a given chain have explicitly consented to being included in the Safe Harbor scope.

However the current implementation has:

```solidity
struct Chain {
    // The address to which recovered assets will be sent.
    string assetRecoveryAddress;
    // The accounts in scope for the agreement.
    Account[] accounts;
    // The CAIP-2 chain ID.
    string caip2ChainId;
    // @audit Missing: signature field as specified in agreement Section 1.1(c)(ii)(D)
}
```
**Impact:** While the `signature` field is described as "optional" in the agreement, its complete omission from the implementation means protocols cannot utilize this feature even if they wish to provide additional evidence of account-level consent for a specific chain.

**Recommended Mitigation:** Consider adding `signature` field to the Chain struct to maintain feature parity with the legal agreement. Alternatively, update the agreement to remove this field.


**SafeHarbor:**
Fixed in [ebfcb1a](https://github.com/PatrickAlphaC/safe-harbor/commit/ebfcb1aa649b67afc758a6b252124b60f99f96c0).

**Cyfrin:** Verified.

\clearpage
