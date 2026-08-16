---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-4-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Resolver Re-derives PDAs Already Computed by Caller, Wasting ~4,500+ CU per
  Resolution
vuln_class: []
---

# Resolver Re-derives PDAs Already Computed by Caller, Wasting ~4,500+ CU per Resolution

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The resolver's account-derivation pipeline calls `Pubkey::find_program_address` 14 times inside `derive_execute_vaa_accounts` (`programs/securitize_bridge/src/resolver.rs:383-632`), spending approximately 1,500 CU per derivation (~21,000 CU total). Three of these PDAs are already derived by the calling function `build_resolved` (`resolver.rs:276-376`) and discarded before the call:

| PDA | `build_resolved` | `derive_execute_vaa_accounts` |
|-----|-------------------|-------------------------------|
| `config_key` (BridgeConfig) | line 288 | line 395 |
| `identity_registry` | line 316 | line 448 |
| `investor` | line 319 | line 466 |

`build_resolved` derives these PDAs to load on-chain state (reading `BridgeConfig` and `ImrInvestor`), then calls `derive_execute_vaa_accounts` which re-derives all three from scratch using the same seeds:

```rust
// build_resolved (resolver.rs:288-291) — first derivation
let (bridge_config_key, _) = Pubkey::find_program_address(
    &[BridgeConfig::SEED_PREFIX, asset_mint.as_ref()],
    program_id,
);

// ... later in build_resolved (resolver.rs:316-326)
let (identity_registry, _) =
    Pubkey::find_program_address(&[asset_mint.as_ref()], &IDENTITY_REGISTRY_ID);

let (investor_key, _) = Pubkey::find_program_address(
    &[
        decoded_payload.investor_id.as_bytes(),
        identity_registry.as_ref(),
        b"Investor",
    ],
    &IDENTITY_METADATA_REGISTRY_ID,
);
```

```rust
// derive_execute_vaa_accounts — redundant re-derivations
let (config_key, _) = Pubkey::find_program_address(      // line 395, dup of 288
    &[BridgeConfig::SEED_PREFIX, asset_mint.as_ref()],
    program_id,
);
// ...
let (identity_registry, _) =                              // line 448, dup of 316
    Pubkey::find_program_address(&[asset_mint.as_ref()], &IDENTITY_REGISTRY_ID);

let (investor, _) = Pubkey::find_program_address(         // line 466, dup of 319
    &[
        investor_id.as_bytes(),
        identity_registry.as_ref(),
        b"Investor",
    ],
    &IDENTITY_METADATA_REGISTRY_ID,
);
```

Additionally, two PDAs use static seeds that never change across invocations:

```rust
// resolver.rs:437-441
let (bridge_event_authority, _) =
    Pubkey::find_program_address(&[SEED_EVENT_AUTHORITY], program_id);

let (rbac_event_authority, _) =
    Pubkey::find_program_address(&[SEED_EVENT_AUTHORITY], &ASSET_CONTROLLER_ID);
```

These could be precomputed as constants or derived once at module level since their seeds are fixed.

**Recommended Mitigation:** Pass the already-derived PDAs from `build_resolved` into `derive_execute_vaa_accounts` as parameters:

```rust
fn derive_execute_vaa_accounts(
    program_id: &Pubkey,
    asset_mint: &Pubkey,
    authorized_user_role: &Pubkey,
    vaa: &VaaFields,
    vaa_hash: &[u8; 32],
    destination_wallet: &Pubkey,
    identity_account: &Pubkey,
    investor_id: &str,
    // New parameters to avoid re-derivation:
    config_key: &Pubkey,
    identity_registry: &Pubkey,
    investor_key: &Pubkey,
) -> Vec<SerializableAccountMeta> {
    // ... use passed-in keys directly ...
}
```

For the static-seed PDAs (`bridge_event_authority`, `rbac_event_authority`), precompute them as module-level constants or use `Pubkey::create_program_address` with a known bump.

**Securitize:** Fixed in [64d336](https://github.com/securitize-io/bc-solana-bridge-sc/commit/64d3363c0caf70f14351205b77ae49b4010f359e).

Accepted the recommendation: config_key, identity_registry, and investor_key are now computed once in build_resolved and passed into derive_execute_vaa_accounts, eliminating the three redundant find_program_address calls.

**Cyfrin:** Confirmed.
