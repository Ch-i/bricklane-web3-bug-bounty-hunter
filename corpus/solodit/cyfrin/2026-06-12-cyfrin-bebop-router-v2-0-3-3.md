---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopValidation::validateSignature` does not enforce canonical low-`s`, accepting
  signature malleability and dual encodings'
vuln_class: []
---

# `BebopValidation::validateSignature` does not enforce canonical low-`s`, accepting signature malleability and dual encodings

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** The EOA (non-contract) branch of `validateSignature` (`contracts/base/BebopValidation.sol:59-67`) accepts both 65-byte standard ECDSA signatures and 64-byte EIP-2098 compact signatures. The 65-byte branch performs no `s`-range check; the 64-byte branch strips only the yParity bit from the `vs` word (`s = vs & UPPER_BIT_MASK`) but does not enforce `s <= 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0`. As a result, for any given signing key and message, two distinct `s` values (one in the lower half, one in the upper half of the curve order) both recover to the same address and both pass validation. Additionally, 64-byte and 65-byte encodings of the same logical signature are each independently valid.

Within `BebopRouter`, replay protection keys on `order.routerNonce` consumed via the bitmap in `BebopValidation::_invalidateNonce`, not on signature bytes. A second presentation of the same order with a malleable signature therefore does not bypass the nonce check and cannot replay a fill on-chain. However, off-chain consumers that key on signature bytes - such as relayers indexing pending settle orders by signature, or any future code path that hashes the signature for deduplication - would treat the two encodings as distinct authorizations for the same order. The absence of canonical-s enforcement is a latent gap as EIP-2098 adoption and off-chain signature indexing grow.

**Recommended Mitigation:** Add a canonical low-`s` check in the 65-byte branch before passing `s` to `ecrecover`: `require(uint256(s) <= 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0)`. OpenZeppelin's `ECDSA::tryRecover` enforces this check and handles both 65-byte and 64-byte EIP-2098 encodings safely; replacing the inline `ecrecover` logic with `ECDSA::tryRecover` (or `SignatureChecker::isValidSignatureNow`) would address malleability and also handle EIP-7702-delegated EOAs in a single change.

**Bebop:** Acknowledged.

\clearpage
