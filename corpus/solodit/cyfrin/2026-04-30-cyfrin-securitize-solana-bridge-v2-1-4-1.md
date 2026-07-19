---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-4-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Unnecessary Heap Clones of `posted.payload` and `WormholeAddresses` in Instruction
  Handlers
vuln_class: []
---

# Unnecessary Heap Clones of `posted.payload` and `WormholeAddresses` in Instruction Handlers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** Two instruction handlers perform full heap clones of structs where lighter access patterns would suffice.

**1. `execute_vaa_v1.rs` — full VAA payload clone (line 257)**

`ExecuteVaaV1::handler` clones the entire VAA payload (up to 1,024 bytes) to a new heap `Vec` before length-checking and decoding it:

```rust
// programs/securitize_bridge/src/instructions/bridge/execute_vaa_v1.rs:257
let payload_bytes = posted.payload.clone();

require_gte!(
    PAYLOAD_MAX_LENGTH,
    payload_bytes.len(),
    BridgeError::InvalidPayload,
);

let decoded_payload =
    abi_decode_bridge_payload(&payload_bytes).ok_or(error!(BridgeError::InvalidPayload))?;
```

Both the length check and `abi_decode_bridge_payload` only require a `&[u8]` reference. The clone allocates up to 1 KB on the heap and copies the full payload before any read occurs.

**2. `update_wormhole_accounts.rs` — `WormholeAddresses` struct clone (line 63)**

`UpdateWormholeAccounts::handler` clones the entire `WormholeAddresses` struct (96 bytes — three `Pubkey` fields) to capture old values before mutation:

```rust
// programs/securitize_bridge/src/instructions/admin/update_wormhole_accounts.rs:63
let old = ctx.accounts.config.wormhole.clone();

require!(
    old.bridge != bridge || old.fee_collector != fee_collector || old.sequence != sequence,
    BridgeError::WormholeAccountsUnchanged,
);

// ... mutate config ...

emit!(WormholeAccountsUpdate {
    old_wormhole_bridge: old.bridge,
    old_wormhole_fee_collector: old.fee_collector,
    old_wormhole_sequence: old.sequence,
    // ...
});
```

The old values could be read into three individual `Pubkey` locals before mutation, avoiding the struct copy entirely.

**Recommended Mitigation:** For the payload, borrow the data directly and decode while the reference is held:

```rust
let payload_bytes = &posted.payload;

require_gte!(
    PAYLOAD_MAX_LENGTH,
    payload_bytes.len(),
    BridgeError::InvalidPayload,
);

let decoded_payload =
    abi_decode_bridge_payload(payload_bytes).ok_or(error!(BridgeError::InvalidPayload))?;
```

For the Wormhole addresses, read individual fields before mutation:

```rust
let old_bridge = ctx.accounts.config.wormhole.bridge;
let old_fee_collector = ctx.accounts.config.wormhole.fee_collector;
let old_sequence = ctx.accounts.config.wormhole.sequence;
```

**Securitize:** payload clone in execute_vaa_v1.rs was already addressed in commit [5cc0158](https://github.com/securitize-io/bc-solana-bridge-sc/commit/5cc01584342e4aaaadc36cf962fd862c81163607) as part of issue [21](https://github.com/securitize-io/bc-solana-bridge-sc/issues/21) - posted.payload is now borrowed, not cloned.

WormholeAddresses clone in update_wormhole_accounts.rs: we agree with the auditor 's comment. WormholeAddresses is composed of three Pubkey ([u8; 32]) fields with no heap-owning members, so .clone() is a 96-byte stack memcpy, not a heap allocation. We propose acknowledging this as not a heap-allocation issue and leaving the code as-is.
