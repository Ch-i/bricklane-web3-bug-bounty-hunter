---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Smart contract wallets cannot sign orders due to missing ERC 1271 support
vuln_class: []
---

# Smart contract wallets cannot sign orders due to missing ERC 1271 support

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `MyriadCTFExchange::_validateOrder` uses `ECDSA.tryRecover` exclusively to validate order signatures. This means only EOAs can sign orders — smart contract wallets (Safe multisigs, Argent, ERC-4337 accounts) cannot participate in the CLOB because they cannot produce ECDSA signatures that recover to their contract address.

```solidity
// MyriadCTFExchange.sol:404-406
(address signer, ECDSA.RecoverError recoverError, ) = ECDSA.tryRecover(orderHash, signature);
require(recoverError == ECDSA.RecoverError.NoError, "invalid signature");
require(signer == order.trader, "signer mismatch");
```

**Impact:** All smart contract wallets — including institutional multisigs, DAOs, and account-abstracted wallets — are excluded from trading on the CLOB. This reduces the protocol's addressable market and excludes participants who use smart contract wallets for security best practices.

**Recommended Mitigation:** Use OpenZeppelin's `SignatureChecker.isValidSignatureNow` which transparently handles both ECDSA and ERC-1271:

```solidity
import "@openzeppelin/contracts/utils/cryptography/SignatureChecker.sol";

require(
    SignatureChecker.isValidSignatureNow(order.trader, orderHash, signature),
    "invalid signature"
);
```

**Myriad:** Fixed in commit [`b8bb04b`](https://github.com/Polkamarkets/polkamarkets-js/commit/b8bb04bfe1d7118c13fd077d2b8cb888a0e971dc)

**Cyfrin:** Verified.
