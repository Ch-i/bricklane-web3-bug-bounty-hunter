---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-2-0
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
title: Transport-Layer Nonce Poisoning Causes Permanent Session Denial of Service
vuln_class: []
---

# Transport-Layer Nonce Poisoning Causes Permanent Session Denial of Service

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The WebSocket transport layer (`websocket/index.ts`) wraps every E2E-encrypted payload in a plaintext `TransportMessage` envelope containing a `clientId (UUID)` and a monotonically-increasing nonce. The deduplication logic on the receiving side accepts any message whose nonce exceeds the highest nonce previously seen for a given `clientId`, then persists the new nonce before the encrypted payload is validated.

Because the Centrifugo relay server allows anonymous connections with no authentication (`allow_anonymous_connect_without_token: true`), any attacker can subscribe to a known channel and observe the plaintext `clientId` and `nonce` fields. The attacker then publishes a single spoofed message with the victim's `clientId` and `nonce` set to `Number.MAX_SAFE_INTEGER (9007199254740991)`. This permanently advances the stored nonce counter so that all subsequent legitimate messages (which have lower, sequential nonces) are silently dropped as "duplicates."

The only pre-requisite for attacker is to have handshake channel name `(handshake:{uuid})` is transmitted in plaintext via the deeplink URL or QR code, making it discoverable.

The `clientId` is discoverable when `TransportMessage` envelope is published as plaintext JSON on the Centrifugo channel. Only the `payload` field is ECIES-encrypted, the `clientId` and `nonce` sit outside the E2E encryption layer.

```ts
// websocket/index.ts _process method
const message: TransportMessage = { clientId, nonce, payload: item.payload };
const data = JSON.stringify(message);
await this.centrifuge.publish(item.channel, data);
```
Any subscriber to the channel reads the clientId directly from the JSON, No decryption needed.

```ts
private async _handleIncomingMessage(channel: string, rawData: string): Promise<void> {
    const message = JSON.parse(rawData) as TransportMessage;
    // ... type checks ...

    if (message.clientId === this.storage.getClientId()) return; // skip own

    const latestNonces = await this.storage.getLatestNonces(channel);
    const latestNonce = latestNonces.get(message.clientId) || 0;

    if (message.nonce > latestNonce) {
        //@audit: Nonce is persisted BEFORE payload validation
        latestNonces.set(message.clientId, message.nonce);
        await this.storage.setLatestNonces(channel, latestNonces);
        this.emit("message", { channel, data: message.payload });
    }
}
```
The issue is that the nonce is updated and persisted to storage unconditionally, regardless of whether the payload subsequently passes E2E decryption in `base-client.ts`. Once persisted, all future legitimate messages with `nonce < MAX_SAFE_INTEGER` are silently dropped.

The DoS is permanent because
- The poisoned nonce is persisted to MMKV via `setLatestNonces`, so it survives app restarts
- The only way to recover is to manually clear the app's storage for this channel
- The victim sees no error as messages are silently dropped as "duplicates"

**Impact:**
- **Handshake channel attack:** An attacker who observes the deeplink URL can subscribe to `handshake:{uuid}`, wait for the wallet to publish its encrypted handshake offer, observe its `clientId`, and immediately publish a nonce-poisoning message. The dApp will advance the nonce, preventing any future communication on the poisoned channel. This is a zero-authentication, single-message DoS.
- **Session channel attack (requires channel discovery):** If the attacker discovers the session channel UUID (e.g., through a prior MITM or relay-side visibility), they can permanently kill an active 30-day session. Neither side can communicate until one creates a completely new session.
- **Persistence across restarts:** Nonces are stored in persistent `IKVStore` (MMKV on mobile), so the DoS survives app restarts and device reboots.


**Proof of Concept:**
1. Attacker observes/gets handshake channel name from the deeplink URL (obtainable via clipboard interception, Android Intent inspection, or QR code scanning), which is plaintext: `metamask://connect/mwp?p=...` containing `channel: "handshake:{uuid}"`.
2. Attacker connects to the Centrifugo relay (no auth token needed). The `WebSocketTransport` constructor in `websocket/index.ts` connects with only reconnect options, no token) and subscribes to that channel.
3. Attacker observes the legitimate peer's `clientId` from any message on the channel. Every message is a plaintext JSON envelope: `{ clientId: "abc-123", nonce: 1, payload: "<encrypted>" }`.
4. Attacker publishes one message: `{ clientId: "abc-123", nonce: 9007199254740991, payload: "x" }`.
5. The victim's `_handleIncomingMessage` (line 233 of `websocket/index.ts`) processes it:
6. All subsequent legitimate messages from `clientId: "abc-123"` with normal sequential nonces (2, 3, 4, ...) hit Number.MAX_SAFE_INTEGER

<details>
<summary>Attached script for poisoning nonce</summary>

```ts
// ============================================================================
// Test: Transport-Layer Nonce Poisoning Causes Permanent Session DoS
// File under test: websocket/index.ts (_handleIncomingMessage, lines 233-258)
// Supporting file: websocket/store.ts (getLatestNonces, setLatestNonces)
// ============================================================================

// Mock KV Store (simulates MMKV persistent storage)
class MockKVStore {
  private store = new Map<string, string>();
  async get(key: string): Promise<string | undefined> {
    return this.store.get(key);
  }
  async set(key: string, value: string): Promise<void> {
    this.store.set(key, value);
  }
  async delete(key: string): Promise<void> {
    this.store.delete(key);
  }
}


// ============================================================================
// Test 1: Nonce poisoning drops all legitimate messages
// ============================================================================

async function test_nonce_poisoning_drops_legitimate_messages() {
  /**
   * Reproduces the exact logic from websocket/index.ts _handleIncomingMessage.
   *
   * Steps:
   *   1. Legitimate message arrives with nonce=1 (accepted)
   *   2. Attacker publishes message with same clientId but nonce=MAX_SAFE_INTEGER
   *   3. Legitimate message arrives with nonce=2 (silently dropped)
   *
   * Root cause: Nonce is persisted (line 248-249) BEFORE the payload reaches
   * base-client.ts for E2E decryption. The attacker's garbage payload fails
   * decryption harmlessly, but the nonce counter is already poisoned.
   */

  const kvstore = new MockKVStore();
  const CHANNEL = "session:test-uuid";
  const NONCE_KEY = `latest-nonces:my-client-id:${CHANNEL}`;
  const emitted: string[] = [];

  // Exact logic from websocket/index.ts lines 233-258
  async function handleIncomingMessage(rawData: string): Promise<void> {
    const message = JSON.parse(rawData);

    // Line 236-238: Type validation
    if (
      typeof message.clientId !== "string" ||
      typeof message.nonce !== "number" ||
      typeof message.payload !== "string"
    ) {
      throw new Error("Invalid message format");
    }

    // Line 241: Skip own messages
    if (message.clientId === "my-client-id") return;

    // Line 244: Load persisted nonces
    const raw = await kvstore.get(NONCE_KEY);
    const latestNonces: Map<string, number> = raw
      ? new Map(Object.entries(JSON.parse(raw)))
      : new Map();

    // Line 245: Get latest nonce for this sender
    const latestNonce = latestNonces.get(message.clientId) || 0;

    // Line 247: Nonce comparison
    if (message.nonce > latestNonce) {
      // Line 248-249: BUG — nonce persisted BEFORE payload validation
      latestNonces.set(message.clientId, message.nonce);
      await kvstore.set(
        NONCE_KEY,
        JSON.stringify(Object.fromEntries(latestNonces))
      );

      // Line 250: Emit to application layer
      emitted.push(message.payload);
    }
    // If nonce <= latestNonce, message is silently dropped as "duplicate"
  }

  // Step 1: Legitimate message (nonce=1) — accepted
  await handleIncomingMessage(
    JSON.stringify({
      clientId: "peer-123",
      nonce: 1,
      payload: "legitimate-encrypted-payload-1",
    })
  );

  // Step 2: Attacker poisons nonce with MAX_SAFE_INTEGER
  await handleIncomingMessage(
    JSON.stringify({
      clientId: "peer-123",
      nonce: Number.MAX_SAFE_INTEGER,
      payload: "garbage-not-valid-ecies",
    })
  );

  // Step 3: Legitimate message (nonce=2) — THIS GETS DROPPED
  await handleIncomingMessage(
    JSON.stringify({
      clientId: "peer-123",
      nonce: 2,
      payload: "legitimate-encrypted-payload-2",
    })
  );

  // Verify: only 2 messages emitted, message [*eciesjs major version mismatch between dApp SDK and mobile wallet creates untested cryptographic interoperability risk*](#eciesjs-major-version-mismatch-between-dapp-sdk-and-mobile-wallet-creates-untested-cryptographic-interoperability-risk) was silently dropped
  const isVulnerable = emitted.length === 2;

  console.log(
    "Test 1 - Nonce poisoning drops legitimate messages:",
    isVulnerable
      ? "VULNERABLE ❌ (Message [*eciesjs major version mismatch between dApp SDK and mobile wallet creates untested cryptographic interoperability risk*](#eciesjs-major-version-mismatch-between-dapp-sdk-and-mobile-wallet-creates-untested-cryptographic-interoperability-risk) silently dropped after nonce poisoning)"
      : "FIXED ✅"
  );
}


// ============================================================================
// Test 2: Poisoned nonce persists across app restarts
// ============================================================================

async function test_nonce_poisoning_persists_across_restarts() {
  /**
   * Proves the DoS is permanent because nonces are stored in persistent
   * KV storage (MMKV on mobile). After an app restart, the poisoned nonce
   * is reloaded and continues to block all legitimate messages.
   *
   * Traces: websocket/store.ts getLatestNonces() and setLatestNonces()
   */

  const kvstore = new MockKVStore();
  const CHANNEL = "session:some-uuid";
  const NONCE_KEY = `latest-nonces:my-client-id:${CHANNEL}`;

  // Simulate: attacker has already poisoned the nonce
  const poisonedNonces = { "peer-123": Number.MAX_SAFE_INTEGER };
  await kvstore.set(NONCE_KEY, JSON.stringify(poisonedNonces));

  // Simulate: app restarts, nonce is reloaded from persistent storage
  const raw = await kvstore.get(NONCE_KEY);
  const restored = new Map<string, number>(Object.entries(JSON.parse(raw!)));
  const storedNonce = restored.get("peer-123") || 0;

  // Simulate: legitimate message arrives after restart with nonce=5
  const legitimateNonce = 5;
  const isDropped = !(legitimateNonce > storedNonce);

  console.log(
    "Test 2 - Poisoned nonce persists across restarts:",
    isDropped
      ? "VULNERABLE ❌ (DoS survives app restart, nonce still poisoned in MMKV)"
      : "FIXED ✅"
  );
}


// ============================================================================
// Test 3: Attacker's garbage payload does not need to pass decryption
// ============================================================================

async function test_nonce_poisoned_before_decryption() {
  /**
   * Proves that the nonce is persisted in _handleIncomingMessage (transport layer)
   * BEFORE the payload reaches decryptMessage in base-client.ts (application layer).
   *
   * The attacker's garbage payload "x" will fail ECIES decryption, but by that
   * point the nonce counter is already written to storage.
   */

  const kvstore = new MockKVStore();
  const CHANNEL = "session:test-uuid";
  const NONCE_KEY = `latest-nonces:my-client-id:${CHANNEL}`;

  // Simulate _handleIncomingMessage with attacker's garbage payload
  const attackerMessage = JSON.stringify({
    clientId: "peer-123",
    nonce: Number.MAX_SAFE_INTEGER,
    payload: "x", // Not valid ECIES ciphertext
  });

  const message = JSON.parse(attackerMessage);

  // Transport layer persists nonce (lines 248-249)
  const latestNonces = new Map<string, number>();
  latestNonces.set(message.clientId, message.nonce);
  await kvstore.set(
    NONCE_KEY,
    JSON.stringify(Object.fromEntries(latestNonces))
  );

  // Application layer tries to decrypt (base-client.ts line 48)
  let decryptionFailed = false;
  try {
    // Simulates: this.keymanager.decrypt("x", privateKey)
    // ECIES decryption of "x" will always fail
    throw new Error("Decryption failed: invalid ciphertext");
  } catch {
    decryptionFailed = true;
  }

  // Check: nonce is already persisted even though decryption failed
  const raw = await kvstore.get(NONCE_KEY);
  const stored = JSON.parse(raw!);
  const nonceAlreadyPoisoned = stored["peer-123"] === Number.MAX_SAFE_INTEGER;

  console.log(
    "Test 3 - Nonce persisted before decryption:",
    decryptionFailed && nonceAlreadyPoisoned
      ? "VULNERABLE ❌ (Nonce written to storage before payload validation)"
      : "FIXED ✅"
  );
}


// ============================================================================
// Runner
// ============================================================================

async function main() {
  console.log("=== Nonce Poisoning DoS Test Suite ===\n");

  await test_nonce_poisoning_drops_legitimate_messages();
  await test_nonce_poisoning_persists_across_restarts();
  await test_nonce_poisoned_before_decryption();

  console.log("\n=== Tests Complete ===");
}

main().catch(console.error);


```

</details>

**Recommended Mitigation:**
1. **Defer nonce persistence until after successful decryption.** Move the `setLatestNonces` call out of `_handleIncomingMessage` and into the application layer (e.g., `base-client.ts`) after the payload has been successfully decrypted and validated. Only update the nonce for messages that pass E2E verification.
2. **Add a maximum nonce jump threshold.** Reject any message where `message.nonce - latestNonce > MAX_NONCE_JUMP` (e.g., 100). Legitimate sequential messages will never jump by thousands.
3. **Consider HMAC authentication on the transport envelope.** Derive a symmetric key from the session's ECDH shared secret and include a MAC over `{clientId, nonce}` in the transport envelope. Only messages with a valid MAC can update the nonce counter.

**Metamask:**
Fixed in commit [fd3a66](https://github.com/MetaMask/mobile-wallet-protocol/commit/fd3a662207b2a2337e89add2a40aec88cbe7cdd2).

**Cyfrin:** Verified.
