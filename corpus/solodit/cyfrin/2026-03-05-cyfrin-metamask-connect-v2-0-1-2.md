---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: No public key validation at handshake and session resumption boundaries
vuln_class: []
---

# No public key validation at handshake and session resumption boundaries

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** At multiple points in the protocol, public keys are accepted and used without structural validation:

1. During the trusted handshake, the received peer public key is stored as raw `base64ToBytes()` output with no curve check
2. During the untrusted handshake, the same pattern applies
3. When resuming a session, stored peer public keys are deserialized from `base64` and passed to `eciesjs` without checks
4. The `KeyManager` classes on both dApp SDK and mobile wallet pass `theirPublicKey` directly to `eciesjs.encrypt()` with no pre-validation

Handshake ingestion (network boundary):
```js
theirPublicKey: base64ToBytes(offer.publicKeyB64)  // No validation
```

Wallet client
```js
theirPublicKey: base64ToBytes(request.publicKeyB64)  // No validation
```

Session resumption (storage boundary):
```js
publicKey: new Uint8Array(Buffer.from(data.keyPair.publicKeyB64, "base64")),
privateKey: new Uint8Array(Buffer.from(data.keyPair.privateKeyB64, "base64")),
theirPublicKey: new Uint8Array(Buffer.from(data.theirPublicKeyB64, "base64")),
```

> No calls to `publicKeyVerify()` exist in this flow

So, a valid `secp256k1` public key must be a point that lies on the curve. Accepting arbitrary byte strings can lead to:
- Invalid curve attacks where the shared secret is predictable
- Crashes or undefined behavior in the native `secp256k1` addon
- Small-subgroup attacks if the key lands on a low-order point

**Impact:**
- A malicious peer sending a crafted `publicKeyB64` can cause `eciesjs` to throw an unhandled exception when the receiving side attempts to encrypt which could crash the connection handler with no user-friendly error.
- Tampered key material in MMKV causes crypto exceptions on session resumption, or an attacker injects a known private key to decrypt session traffic.
- If `expiresAt` is corrupted to `NaN`, `NaN < Date.now()` evaluates to `false`, so the session never expires and could persist indefinitely beyond the intended 30-day TTL.

**Recommended Mitigation:**
- Validate all received public keys with `secp256k1.publicKeyVerify()` before use
- Validate keys both at handshake time and when loading from session storage by creating a shared validation utility in `core/src/domain/`:
```js
export function validateSecp256k1PublicKey(key: Uint8Array): void {
    if (key.length !== 33) throw new CryptoError(...);
    if (key[0] !== 0x02 && key[0] !== 0x03) throw new CryptoError(...);
}
```
- Apply in `_createFinalSession`, `_createSession`, `SessionStore.get`, and both `KeyManager` implementations.
- Add `isNaN(expiresAt)` check in session store deserialization.
- Reject and terminate the session if validation fails

**MetaMask:** Fixed in [commit](https://github.com/MetaMask/mobile-wallet-protocol/commit/bcb426c465ca3391361163191c9d58773df961c5).

**Cyfrin:** Verified.
