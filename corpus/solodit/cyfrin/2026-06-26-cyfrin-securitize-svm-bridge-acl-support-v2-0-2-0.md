---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: Redundant heap clone of the up-to-1024-byte VAA payload on every inbound bridge
  transaction
vuln_class: []
---

# Redundant heap clone of the up-to-1024-byte VAA payload on every inbound bridge transaction

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** `validate_and_decode_vaa` deliberately `core::mem::take`s the raw payload bytes out of `PostedVaaData` into `DecodedVaa::posted_payload_bytes` "to avoid an extra heap copy" - but `finalize_inbound_vaa` then immediately `.clone()`s that buffer back into `received.payload`. Because `DecodedVaa` is passed to `finalize_inbound_vaa` by shared reference (`&decoded`) and the `posted_payload_bytes` field is never read again by either inbound handler after this call (both `execute_vaa_v1` and `execute_vaa_v1_spl` only read `decoded.payload.*` / `decoded.posted_emitter_chain` afterwards), the clone is pure waste: a heap allocation plus a memcpy of up to `PAYLOAD_MAX_LENGTH` (1024) bytes on every inbound bridge execution (a hot, per-transaction path).

```
bc-solana-bridge-sc/programs/securitize_bridge/src/utils/validate_and_decode_vaa.rs
76:        posted_payload_bytes: core::mem::take(&mut posted_vaa.payload),
97:    received.payload = decoded.posted_payload_bytes.clone();
```

Call sites confirming the field is not reused after `finalize_inbound_vaa`:

```
bc-solana-bridge-sc/programs/securitize_bridge/src/instructions/bridge/execute_vaa_v1.rs
232:    finalize_inbound_vaa(
257:    emit_cpi!(DsTokenBridgeReceive { ... decoded.payload.* ... })

bc-solana-bridge-sc/programs/securitize_bridge/src/instructions/bridge/execute_vaa_v1_spl.rs
177:    finalize_inbound_vaa(
187:    emit_cpi!(SplTokenBridgeReceive { ... decoded.payload.* ... })
```

**Recommended Mitigation:** Move the buffer instead of cloning it. Change `finalize_inbound_vaa` to take the payload bytes by value (or to take `&mut DecodedVaa` and `core::mem::take` the field), so the already-owned `Vec<u8>` is moved straight into `received.payload`:

```rust
pub fn finalize_inbound_vaa(
    consumed_vaa: &mut Account<ConsumedVaa>,
    received: &mut Account<Received>,
    recipient_wallet: &Pubkey,
    decoded: &mut DecodedVaa,   // was &DecodedVaa
    vaa_hash: [u8; 32],
) -> Result<()> {
    // ... existing checks (read decoded.destination_wallet etc.) ...
    received.payload = core::mem::take(&mut decoded.posted_payload_bytes); // no clone
    Ok(())
}
```

The `take` already on line 76 plus the move here makes the whole inbound path move-only for the payload buffer. The `emit_cpi!` blocks that follow do not touch `posted_payload_bytes`, so emptying it is safe.

**Securitize:** Fixed in commit [5b4982a1bb](https://github.com/securitize-io/bc-solana-bridge-sc/commit/5b4982a1bbaa39a5fa963072983e0bad4fb273f3). finalize_inbound_vaa now takes decoded: &mut DecodedVaa and moves the payload buffer into received.payload via core::mem::take(&mut decoded.posted_payload_bytes) instead of cloning it. Combined with the existing take out of PostedVaaData, the whole inbound path is now move-only for the payload buffer — the up-to-1024-byte heap allocation with memcpy per inbound transaction is eliminated. Behavior is unchanged.

**Cyfrin:** Verified.

\clearpage
