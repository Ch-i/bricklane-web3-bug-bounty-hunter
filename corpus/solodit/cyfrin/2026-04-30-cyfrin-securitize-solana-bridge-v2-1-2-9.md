---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Emitter rotation can strand old VAAs and collide with new-emitter sequence
  numbers
vuln_class: []
---

# Emitter rotation can strand old VAAs and collide with new-emitter sequence numbers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The trusted foreign emitter for a source chain is stored in a single `EmitterAddress` PDA keyed only by `["emitter_address", asset_mint, emitter_chain]`.

```rust

```49:58:programs/securitize_bridge/src/instructions/bridge/execute_vaa_v1.rs
    /// Expected VAA emitter for `emitter_chain` (mirrors EVM `emitterAddresses`).
    #[account(
        seeds = [
            EmitterAddress::SEED_PREFIX,
            config.asset_mint.as_ref(),
            &emitter_chain.to_le_bytes(),
        ],
        bump = emitter_address.bump,
        constraint = emitter_address.address != ZERO_ADDRESS @ BridgeError::EmitterAddressNotConfigured,
    )]
    pub emitter_address: Box<Account<'info, EmitterAddress>>,
```

`set_emitter_address` overwrites the single trusted emitter for `(asset_mint, emitter_chain)`, so `execute_vaa_v1` immediately stops accepting VAAs from the previous emitter.

```rust
    let emitter_address = &mut ctx.accounts.emitter_address;
    emitter_address.chain = chain;
    emitter_address.address = address;
    emitter_address.bump = ctx.bumps.emitter_address;
```


Execution additionally requires the posted VAA’s `emitter_address` to match that stored value.

```rust
    // Require posted VAA emitter address matches registered peer for this source chain.
    require!(
        ctx.accounts
            .emitter_address
            .verify(posted.emitter_address()),
```

Also, `Received` accounts are initialized with seeds that include sequence but **not** emitter bytes:

```rust
    #[account(
        init,
        payer = payer,
        seeds = [
            Received::SEED_PREFIX.as_ref(),
            config.asset_mint.as_ref(),
            emitter_chain.to_le_bytes().as_ref(),
            sequence.to_le_bytes().as_ref(),
        ],
        bump,
        space = 8 + Received::INIT_SPACE,
    )]
    pub received: Box<Account<'info, Received>>,
```

If the replacement emitter starts its Wormhole sequence from a value already used by the previous emitter, `execute_vaa_v1` will fail because the corresponding Received PDA already exists, even though the VAA hash is different.

**Impact:**
- Old VAAs already in flight can become unexecutable after emitter rotation.
- If the new emitter reuses sequence numbers already consumed under the old emitter, some new VAAs may also be unexecutable on Solana.

**Recommended Mitigation:** Document how emitter updates: pause or drain in-flight inbound VAAs, coordinate with relayers and the source chain, and define how users recover stuck operations.

**Securitize:** Fixed in [fac534](https://github.com/securitize-io/bc-solana-bridge-sc/commit/fac534095f93d05a229665b16aec950ec8bdb5e7).

**Cyfrin:** Verified.
