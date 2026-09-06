---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: Session expiry not enforced on inbound message path
vuln_class: []
---

# Session expiry not enforced on inbound message path

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The `BaseClient` checks session expiry only on the outbound send path via `checkSessionExpiry()` not on the inbound receive path:

```js
// packages/core/src/base-client.ts:46-50
this.transport.on("message", async (payload) => {
    if (!this.session?.keyPair.privateKey) return;   // Null check only, no expiry check
    const message = await this.decryptMessage(payload.data);
    if (message) this.handleMessage(message);
});
```

Whereas every outgoing message enforces expiry:

```js
// packages/core/src/base-client.ts:140-142
protected async sendMessage(channel: string, message: ProtocolMessage): Promise<void> {
    if (!this.session) throw new SessionError(...);
    await this.checkSessionExpiry();   // Enforced here
    ...
}
```

This creates a brief asymmetric window after a session's `expiresAt` timestamp passes: inbound messages are still decrypted and emitted to the application layer while outbound messages are correctly blocked.

**Impact:** The practical exploitability of this gap is minimal for several reasons:

1. **The response path blocks exploitation.** On the wallet side, the full message lifecycle is: receive → decrypt → `handleMessage()` → emit `"message"` → `RPCBridgeAdapter` → `BackgroundBridge` processes request → generates response → `client.sendResponse()` → `sendMessage()` → `checkSessionExpiry()` → **`SESSION_EXPIRED` thrown**. The response can never be delivered back to the dApp. Any request processed on an expired session produces a result that is discarded at the send boundary.

2. **Both peers share the same `expiresAt`.** The dApp client has the same TTL and the same `checkSessionExpiry()` guard on its `sendMessage()`. For the dApp to send a request to an expired wallet session, its own session must also be expired meaning its own `sendMessage()` would throw first. The only way around this is clock skew between devices.

3. **The transport won't survive the TTL.** With a 30-day `DEFAULT_SESSION_TTL`, a mobile app backgrounded for that duration will have long since lost its WebSocket connection. Resuming via `client.resume()` calls `sessionstore.get()`, which checks expiry and returns `null` for expired sessions preventing reconnection.

4. **Sensitive operations are approval-gated.** All state-changing wallet operations (transactions, signing, `wallet_createSession`) require user interaction through `ApprovalController` before execution. The user prompt itself acts as an additional gate before any side effects occur.

**Recommended Mitigation:** Add an expiry check to the inbound message handler for defense-in-depth:

```js
// packages/core/src/base-client.ts - constructor
this.transport.on("message", async (payload) => {
    if (!this.session?.keyPair.privateKey) return;
    if (this.session.expiresAt < Date.now()) {
        await this.disconnect();
        return;
    }
    const message = await this.decryptMessage(payload.data);
    if (message) this.handleMessage(message);
});
```
**MetaMask:** Fixed in this [PR](https://github.com/MetaMask/mobile-wallet-protocol/pull/72).

**Cyfrin:** Verified.

\clearpage
