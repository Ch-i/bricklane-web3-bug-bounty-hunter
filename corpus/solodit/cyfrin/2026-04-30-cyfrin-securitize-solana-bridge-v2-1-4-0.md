---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-4-0
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
title: Instruction Handlers Use `find_program_address` Where Cheaper Derivation Is
  Available
vuln_class: []
---

# Instruction Handlers Use `find_program_address` Where Cheaper Derivation Is Available

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** Several instruction handlers call `Pubkey::find_program_address` at runtime to derive PDAs whose bumps are either already available from the Anchor context or could be obtained via Anchor `seeds + bump` constraints. `find_program_address` iterates bump values starting from 255 downward until it finds a valid off-curve address, costing ~1,500 CU per call. The cheaper alternative, `Pubkey::create_program_address`, uses a known bump directly for ~200 CU.

The affected call sites are:

**1. `initialize.rs` — bridge authority bump (line 115)**

```rust
// programs/securitize_bridge/src/instructions/admin/initialize.rs:115-121
let (_, bridge_authority_bump) = Pubkey::find_program_address(
    &[SEED_PREFIX_BRIDGE_AUTHORITY, ctx.accounts.asset_mint.key().as_ref()],
    ctx.program_id,
);
```

The `bridge_authority` PDA could be declared as an `UncheckedAccount` with `seeds + bump` in the `Initialize` accounts struct. Anchor would then derive the bump via `find_program_address` once during account validation, and the handler could read it from `ctx.bumps.bridge_authority` at zero additional cost.

**2. `initialize.rs` — RBAC validation PDAs (lines 148, 160)**

```rust
// initialize.rs:148-151
let (expected_asset_access_controller, _) = Pubkey::find_program_address(
    &[mint.key().as_ref(), SEED_ASSET_ACCESS_CONTROLLER],
    &RBAC_PROGRAM_ID,
);

// initialize.rs:160-161
let (expected_controller_authority, _) =
    Pubkey::find_program_address(&[asset_access_controller.key().as_ref()], &RBAC_PROGRAM_ID);
```

These are cross-program PDAs used only for key comparison. If the accounts were declared with `seeds` constraints (using `seeds::program`), Anchor would handle the derivation. Alternatively, bumps could be passed as instruction arguments.

**3. `bridge_ds_tokens.rs` — wormhole message PDA (line 254)**

```rust
// programs/securitize_bridge/src/instructions/bridge/bridge_ds_tokens.rs:254-258
let (expected_wormhole_message, wormhole_message_bump) = Pubkey::find_program_address(
    &[
        SEED_PREFIX_SENT,
        config.asset_mint.as_ref(),
        &outgoing_sequence.to_le_bytes()[..],
    ],
    // ...
);
```

The sequence-dependent seed makes this PDA dynamic per invocation, but the bump could still be passed as an instruction argument to avoid the search.

**4. `execute_vaa_v1.rs` — RBAC event authority (line 228)**

```rust
// programs/securitize_bridge/src/instructions/bridge/execute_vaa_v1.rs:228-229
let (expected_rbac_event_authority, _) =
    Pubkey::find_program_address(&[SEED_EVENT_AUTHORITY], &ASSET_CONTROLLER_ID);
```

This uses a fixed seed and a fixed program ID — the result is a constant that could be precomputed at build time.

**Recommended Mitigation:**
- For PDAs owned by the bridge program (`bridge_authority`, `wormhole_message`): declare them in the Anchor accounts struct with `seeds + bump` constraints and read bumps from `ctx.bumps`.
- For cross-program PDAs used only for validation (`asset_access_controller`, `controller_authority`): either use `seeds::program` constraints or accept bumps as instruction arguments and verify with `create_program_address`.
- For static-seed PDAs (`rbac_event_authority`): precompute as a module-level constant.

**Securitize:** Fixed in [164abab](https://github.com/securitize-io/bc-solana-bridge-sc/commit/164abab15f609097097849509df4f09429e0f8ca).

**Cyfrin:** Verified.
