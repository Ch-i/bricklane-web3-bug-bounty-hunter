---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: Unvalidated `initialMessage` enables cross-dApp approval griefing
vuln_class: []
---

# Unvalidated `initialMessage` enables cross-dApp approval griefing

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The SessionRequest type includes an optional `initialMessage` field which is an intentional protocol feature designed to solve the "dApp suspension" problem on mobile. Since iOS/Android may suspend the dApp process immediately after launching the deeplink, the dApp embeds its first RPC call directly in the plaintext connection request so the wallet can begin processing it without waiting for a round-trip response:

```ts
initialMessage?: Message;  // Message = { type: "message"; payload: unknown }
```

After completing the trusted handshake the wallet dispatches `initialMessage` directly into the normal message pipeline, bypassing E2E encryption entirely:
```ts
public async execute(session: Session, request: SessionRequest): Promise<void> {
    await this._finalizeConnection(request.channel); //@audit-info session marked CONNECTED
    this._processInitialMessage(request.initialMessage);
}
...
//@audit-info handling initial message downstream with handleMessage
private _processInitialMessage(message?: Message): void {
    if (!message) return;
    setTimeout(() => this.context.handleMessage(message), 0);
}
```

`WalletClient.handleMessage` then emits any `{ type: "message" }` onto the "message" event. So when a new SDK connection deeplink triggers a `wallet_createSession` request and there are existing pending approval requests in the MetaMask wallet's `ApprovalController`, the Connection class automatically rejects ALL pending approvals without user consent. This is design choice as stated in comments and done as a "cleanup" measure to avoid stale approvals :

```ts
this.client.on('message', async (payload) => {
    const isWalletCreateSessionRequest =
        payload && typeof payload === 'object' &&
        'name' in payload &&
        payload.name === 'metamask-multichain-provider' &&
        'data' in payload &&
        payload.data && typeof payload.data === 'object' &&
        'method' in payload.data &&
        payload.data.method === 'wallet_createSession';

    if (
        isWalletCreateSessionRequest &&
        Engine.context.ApprovalController.getTotalApprovalCount() > 0
    ) {
        // Force-navigates away from current screen
        NavigationService.navigation?.goBack();
        // Rejects ALL pending approvals as "userRejectedRequest"
        await Engine.context.ApprovalController.clear(
            providerErrors.userRejectedRequest({
                data: { cause: 'rejectAllApprovals' },
            }),
        );
    }
    this.bridge.send(payload);
});
```
However, it creates a griefing vector against legitimate in-progress transactions. An attacker can craft a valid MWP connection deeplink and deliver it to the victim (via link, message, or QR code). When the victim opens it, their MetaMask wallet will automatically reject any transaction signing request, permission approval, or other pending confirmation they may be in the process of reviewing, including approvals for completely unrelated dApps.



**Impact:**
1. Transaction griefing: If a user is reviewing a high-value DeFi transaction approval, an attacker can force-reject it by sending the victim a deeplink. The user's pending transaction is rejected as `userRejectedRequest`, and the dApp receives an error response indistinguishable from a deliberate user rejection.
2. Time-sensitive attack: For time-limited operations (e.g., token swaps with slippage deadlines, auction bids, liquidation protections), the forced rejection could cause financial loss.
3. No user awareness: The rejection happens programmatically. The user sees the approval screen disappear and is navigated away. There is no confirmation dialog or indication that the rejection was triggered by an external deeplink rather than their own action.
4. Cross-dApp impact: The `ApprovalController.clear()` call rejects ALL pending approvals from ALL dApps, not just the one associated with the incoming connection.

**Proof of Concept:** <details>
<summary>Add to <code>connection.test.ts</code></summary>

```ts

 // M-01 PoC: isConnectionRequest() (connection-request.ts:43-55) does not validate
  // initialMessage, so an attacker embeds wallet_createSession in a deeplink.
  // ApprovalController.clear() (connection.ts:66-72) then rejects ALL pending approvals
  // system-wide. TrustedConnectionHandler completes the handshake unilaterally —
  // victim only needs to open the URL.
  describe('Security PoC: initialMessage griefing via crafted deeplink', () => {
    const craftedInitialMessagePayload = {
      name: 'metamask-multichain-provider',
      data: { method: 'wallet_createSession', id: 'attacker-req-1', jsonrpc: '2.0' },
    };

    it('[POC-1] crafted initialMessage triggers ApprovalController.clear(), rejecting ALL pending approvals across ALL dApps', async () => {
      await Connection.create(mockConnectionInfo, mockKeyManager, RELAY_URL, mockHostApp);
      (Engine.context.ApprovalController.getTotalApprovalCount as jest.Mock).mockReturnValue(3);

      // Simulates trusted-connection-handler.ts:78 → WalletClient.emit("message") path
      await onClientMessageCallback(craftedInitialMessagePayload);

      expect(NavigationService.navigation?.goBack).toHaveBeenCalledTimes(1);
      expect(Engine.context.ApprovalController.clear).toHaveBeenCalledTimes(1);
      expect(Engine.context.ApprovalController.clear).toHaveBeenCalledWith(
        providerErrors.userRejectedRequest({ data: { cause: 'rejectAllApprovals' } }),
      );
      expect(mockBridgeInstance.send).toHaveBeenCalledWith(craftedInitialMessagePayload);
    });

    it('[POC-2] isConnectionRequest() accepts a deeplink with malicious initialMessage — not blocked at the parser', () => {
      // isConnectionRequest() never inspects initialMessage (connection-request.ts:43-55)
      const { isConnectionRequest } = jest.requireActual<
        typeof import('../types/connection-request')
      >('../types/connection-request');

      const maliciousConnectionRequest = {
        sessionRequest: {
          id: 'attacker-session-id',
          publicKeyB64: 'AoBDLWxRbJNe8yUv5bmmoVnNo8DCilzbFz/nWD+RKC2V',
          channel: 'handshake:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
          mode: 'trusted',
          expiresAt: Date.now() + 60_000,
          initialMessage: { type: 'message', payload: craftedInitialMessagePayload },
        },
        metadata: {
          dapp: { name: 'Legitimate App', url: 'https://legitimate-app.com' },
          sdk: { version: '1.0.0', platform: 'web' },
        },
      };

      expect(isConnectionRequest(maliciousConnectionRequest)).toBe(true);
      expect(
        (maliciousConnectionRequest.sessionRequest as any).initialMessage.payload.data.method,
      ).toBe('wallet_createSession');
    });

    it('[POC-3] non-wallet_createSession initialMessage does NOT trigger ApprovalController.clear() — attack requires exactly this method', async () => {
      await Connection.create(mockConnectionInfo, mockKeyManager, RELAY_URL, mockHostApp);
      (Engine.context.ApprovalController.getTotalApprovalCount as jest.Mock).mockReturnValue(3);

      const benignPayload = {
        name: 'metamask-multichain-provider',
        data: { method: 'eth_sendTransaction', id: 'req-2', jsonrpc: '2.0' },
      };

      await onClientMessageCallback(benignPayload);

      expect(Engine.context.ApprovalController.clear).not.toHaveBeenCalled();
      expect(NavigationService.navigation?.goBack).not.toHaveBeenCalled();
      expect(mockBridgeInstance.send).toHaveBeenCalledWith(benignPayload);
    });
  });

```
</details>

**Recommended Mitigation:**
1. Never auto-reject pending approvals. Instead of that, queue the new `wallet_createSession` request and present it to the user after they have resolved (approved or rejected) their current pending approval.
2. Scope approval rejection to the specific connection. If cleanup is necessary, only reject approvals originating from the same dApp `origin`, not from ALL dApps via the global `ApprovalController.clear()`.
3. Require user confirmation before clearing approvals. If the design requires replacing the current approval, show a confirmation dialog: "A new connection request was received. Dismiss current pending approval?"

**Metamask:**
Acknowledged; we accept this tradeoff for the UX reliability it provides. We may revisit scoping the approval clearance to same-origin connections in a future iteration if the underlying approval rendering issues are resolved upstream.
