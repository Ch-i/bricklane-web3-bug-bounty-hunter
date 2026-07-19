---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: Internal origin allowlist bypass via unnormalized URL matching in ConnectionRegistry
vuln_class: []
---

# Internal origin allowlist bypass via unnormalized URL matching in ConnectionRegistry

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The `ConnectionRegistry.handleConnectDeeplink()` method validates incoming connection requests against a static list of internal origins using `Array.includes()` which performs exact string comparison. The values being compared (`connReq.metadata.dapp.ur`l and `connReq.metadata.dapp.name`) are self-reported by the connecting dApp through the deeplink payload and are never verified against any external source.

```js
if (
  INTERNAL_ORIGINS.includes(connReq.metadata.dapp.url) ||
  INTERNAL_ORIGINS.includes(connReq.metadata.dapp.name)
) {
  throw rpcErrors.invalidParams({
    message: 'External transactions cannot use internal origins',
  });
}
```
The `connReq.metadata` comes directly from a deeplink payload:
```js
const connReq: unknown = JSON.parse(jsonString);
```

This metadata is attacker controlled. There is no normalization, canonicalization, or sanitization before the `includes()` comparison. An attacker controlled dApp can bypass this check by submitting a `URL` that is semantically equivalent to an internal origin but differs at the string level.

Examples:
```
https://metamask.io/ vs https://metamask.io     (trailing slash)
https://MetaMask.io vs https://metamask.io      (casing)
https://metamask.io/./                          (dot segment)
https://metamаsk.io                             (cyrillic 'а' U+0430 vs latin 'a' U+0061)
```

**Impact:** A malicious dApp can set its metadata to closely resemble a trusted MetaMask internal `origin` bypassing the blocklist and displaying a spoofed origin string in the wallet approval UI. This is a UI deception issue. It does not bypass transaction approval since the wallet still requires explicit user confirmation for every action and the user sees actual transaction details (recipient, amount, contract data) in the approval screen.

**Recommended Mitigation:** Normalize URLs before comparison. At minimum, lowercase both sides, strip trailing slashes, and resolve relative path segments. Consider using prefix or pattern matching rather than exact string equality. As a broader point, treat all dApp-reported metadata as untrusted input and avoid using it as the sole basis for any security decision.

```js
private isInternalOrigin(origin: string): boolean {
  try {
    const normalized = new URL(origin).origin.toLowerCase();
    return INTERNAL_ORIGINS.some(
      (internal) => new URL(internal).origin.toLowerCase() === normalized,
    );
  } catch {
    return false;
  }
}
```

Then replace the current check:
```js
if (
  this.isInternalOrigin(connReq.metadata.dapp.url) ||
  INTERNAL_ORIGINS.some(
    (o) => o.toLowerCase() === connReq.metadata.dapp.name.toLowerCase(),
  )
) {
  throw rpcErrors.invalidParams({
    message: 'External transactions cannot use internal origins',
  });
}
```

**MetaMask:** Fixed in commits [ca66895](https://github.com/MetaMask/metamask-mobile/commit/ca668952d2d80352560f193d7dd2e22aed7ae4e9), [b60153](https://github.com/MetaMask/metamask-mobile/commit/b6015313dba44592814e58f2e9612e585852de14).

**Cyfrin:** Verified.

\clearpage
