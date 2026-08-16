---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: Session object with private key, decrypted payloads logged in debug mode and
  deeplink url being logged unconditionally on error path
vuln_class: []
---

# Session object with private key, decrypted payloads logged in debug mode and deeplink url being logged unconditionally on error path

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** Debug-level logging outputs full session objects (including private keys) and decrypted message payloads. Additionally, one error path logs the raw deeplink URL unconditionally, which may contain sensitive connection parameters.

1. When debug logging is enabled, the dApp SDK logs the full `session` object (which contains `keyPair.privateKey`) via `logger('active session found', session)`. The mobile wallet logs decrypted JSON-RPC payloads via `logger.debug('Received message:', payload)` and `logger.debug('Sending message:', payload)`.

On mobile devices, these logs can be accessible via crash reporters, log aggregation, or ADB logcat.

2. When deeplink parsing fails, the raw deeplink URL is logged at the error level regardless of debug mode. Deeplink URLs contain connection parameters (channel ID, public key) that could be used to intercept or replay connections.
```js
logger.error('Failed to handle connect deeplink:', error, url);
```
```js
error: (...args: unknown[]) => {
    console.error(prefix, ...args);  // Always active, no debug gate
},
```

**Impact:**
- Private key exposure via device logs, crash reporters, or log aggregation
- Decrypted transaction details (addresses, amounts) visible in logs
- Connection parameters leaked on error paths even in production builds

**Recommended Mitigation:**
- Create a safe session serializer that excludes keyPair:
```js
function safeSessionLog(session: Session) {
    return { id: session.id, channel: session.channel, expiresAt: session.expiresAt };
}
```
- Redact message payloads in debug logs to metadata only.
- Gate `logger.error` calls containing URLs behind the debug flag, or strip query parameters before logging.


**MetaMask:** Fixed in commits [e9e2ad](https://github.com/MetaMask/connect-monorepo/commit/e9e2ade076ae56ba2264937a1fb68339025b319b), [be2b91](https://github.com/MetaMask/metamask-mobile/commit/be2b91ce59f2f3caeb10a322b7b26251380f3aba)

**Cyfrin:** Verified.
