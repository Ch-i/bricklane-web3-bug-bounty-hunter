---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-12
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopValidation::validateSignature` rejects 65-byte ECDSA signatures that
  encode v as 0 or 1'
vuln_class: []
---

# `BebopValidation::validateSignature` rejects 65-byte ECDSA signatures that encode v as 0 or 1

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `validateSignature` handles 65-byte signatures by reading `v = uint8(signature[64])` verbatim and passing it directly to `ecrecover`:

```solidity
// contracts/base/BebopValidation.sol:59-72
if (signature.length == 65) {
    (r, s) = abi.decode(signature, (bytes32, bytes32));
    v = uint8(signature[64]);
} else if (signature.length == 64) {
    // EIP-2098
    bytes32 vs;
    (r, vs) = abi.decode(signature, (bytes32, bytes32));
    s = vs & UPPER_BIT_MASK;
    v = uint8(uint256(vs >> 255)) + 27;
}
...
address signer = ecrecover(hash, v, r, s);
require(signer != address(0), InvalidSignature());
```

The 64-byte EIP-2098 branch normalizes the recovery bit to `v` in `{27, 28}`, but the 65-byte branch does not. Signatures encoded with `v` in `{0, 1}` are common in some signing libraries as the raw recovery ID. Those signatures recover the expected signer if normalized by adding 27, but in this implementation `ecrecover` returns `address(0)` and validation reverts with `InvalidSignature`.

**Files:**

- `contracts/base/BebopValidation.sol` - `BebopValidation::validateSignature`

**Impact:** Signers whose libraries emit 65-byte signatures with raw `v` values in `{0, 1}` cannot authenticate through the 65-byte path. The same underlying signature succeeds if re-encoded with `v` in `{27, 28}` or converted to the supported EIP-2098 format.

**Recommended Mitigation:** Normalize `v` in the 65-byte branch before passing to `ecrecover`:

```solidity
if (signature.length == 65) {
    (r, s) = abi.decode(signature, (bytes32, bytes32));
    v = uint8(signature[64]);
    if (v < 27) v += 27; // normalize {0,1} -> {27,28}
}
```

This mirrors the behavior of OpenZeppelin's ECDSA library and eliminates the asymmetry between the 64-byte and 65-byte paths.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.
