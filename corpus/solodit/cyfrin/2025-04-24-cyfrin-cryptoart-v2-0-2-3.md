---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: '`MintType` is almost never enforced'
vuln_class: []
---

# `MintType` is almost never enforced

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** The contract has an enumeration `MintType` which defines several types of mints:
```solidity
enum MintType {
    OpenMint,
    Whitelist,
    Claim,
    Burn
}
```

But there are never any checks for these mint types, for example:
* there is no check for `MintType.Whitelist` and no corresponding whitelist enforcement
* the `claim` function doesn't enforce input `data.mintType == MintType.Claim`
* similarly `burnAndMint` doesn't enforce input `data.mintType == MintType.Burn`

The only place input `data.mintType` is used is in `_validateSignature` to validate that the input parameter matches what was signed, but there is no other validation that the correct mint types are being used for the correct operations.

**CryptoArt:**
Fixed in commit [deaf964](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/deaf96420b3176be09c1522ea8c79a211f77ef82).

**Cyfrin:** Verified.
