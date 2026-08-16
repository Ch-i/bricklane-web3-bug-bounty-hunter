---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: Weak structural validation of connectionRequest from deeplink
vuln_class: []
---

# Weak structural validation of connectionRequest from deeplink

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The `ConnectionRequest` parsed from deeplinks undergoes minimal structural validation. Required fields are checked for presence and type but not for format, length, or semantic correctness.

When a deeplink is received, its parameters are parsed into a `ConnectionRequest`. The validation checks:
- `mode`: verified as `typeof string` only, not validated against `["trusted", "untrusted"]`
- `id`: verified as `typeof string`, and not validated againt `UUID` format validation
- `publicKeyB64`: checked for presence but no format/length validation
- `channel` with `typeof string` and no `handshake:{uuid}` format check
- `expiresAt`: checked as `typeof number` but no `isNaN` or future-time check
- `dapp.name`, `dapp.url` , `url`:  validated as URL format but no length cap on either field

For example:
An invalid mode value (e.g., "invalid") passes validation and at `dapp-client` and `wallet-client` the ternary `mode === "trusted" ? TrustedConnectionHandler : UntrustedConnectionHandler` defaults to `UntrustedConnectionHandler` which is the more secure path (a safe failure mode). This allows malformed or adversarial values to enter the system which in-future may cause unexpected behavior in downstream processing.

**Impact:**
- Malformed but structurally valid connection requests proceed into the connection flow. An arbitrarily long `dapp.name` (megabytes) could cause UI rendering issues when displayed in the connection approval dialog.
- `NaN` `expiresAt` values propagate through without detection.
- Increases attack surface by accepting inputs that should be rejected early

**Recommended Mitigation:**
- Validate `mode` against allowed enum values (`"trusted"`, `"untrusted"`)
- Validate `publicKeyB64` format (base64 string decoding to correct byte length for `secp256k1`)
- Add `isNaN` guard on `expiresAt` and verify it's a future timestamp
```js
if (!['trusted', 'untrusted'].includes(sessionReq.mode)) return false;
if (isNaN(sessionReq.expiresAt) || sessionReq.expiresAt < Date.now()) return false;
if (sessionReq.publicKeyB64.length > 200) return false;
if (metadata.dapp.name.length > 256) return false;
```
- Enforce maximum length bounds on all string fields

**MetaMask:** Fixed in commit [ca6689](https://github.com/MetaMask/metamask-mobile/commit/ca668952d2d80352560f193d7dd2e22aed7ae4e9).

**Cyfrin:** Verified.
