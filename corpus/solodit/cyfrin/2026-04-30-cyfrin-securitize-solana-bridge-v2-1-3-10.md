---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-10
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`update_wormhole_accounts` is for recovery, or for migration after a bridge
  upgrade, not for routine reconfiguration'
vuln_class: []
---

# `update_wormhole_accounts` is for recovery, or for migration after a bridge upgrade, not for routine reconfiguration

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `update_wormhole_accounts` is a constrained recovery hook, and only supports migration in conjunction with a bridge program upgrade. It's not a routine reconfiguration mechanism.

`initialize` fixes the Wormhole-related accounts to canonical PDA-derived addresses under the Wormhole program, and `update_wormhole_accounts` applies the same constrained validation.

```rust
    pub wormhole_program: Program<'info, wormhole::program::Wormhole>,

    #[account(
        mut,
        seeds = [wormhole::BridgeData::SEED_PREFIX],
        bump,
        seeds::program = wormhole_program.key,
    )]
    pub wormhole_bridge: Box<Account<'info, wormhole::BridgeData>>,

    #[account(
        mut,
        seeds = [wormhole::FeeCollector::SEED_PREFIX],
        bump,
        seeds::program = wormhole_program.key,
    )]
    pub wormhole_fee_collector: Box<Account<'info, wormhole::FeeCollector>>,

    // ... wormhole_emitter ...

    #[account(
        mut,
        seeds = [
            wormhole::SequenceTracker::SEED_PREFIX,
            wormhole_emitter.key().as_ref(),
        ],
        bump,
        seeds::program = wormhole_program.key,
    )]
    pub wormhole_sequence: UncheckedAccount<'info>,
```

`update_wormhole_accounts` uses the same pattern: the passed accounts must be the canonical PDAs for the supplied `wormhole_program` and the mint’s `wormhole_emitter`:

```rust
    pub wormhole_program: Program<'info, wormhole::program::Wormhole>,

    #[account(
        mut,
        seeds = [wormhole::BridgeData::SEED_PREFIX],
        bump,
        seeds::program = wormhole_program.key,
    )]
    pub wormhole_bridge: Box<Account<'info, wormhole::BridgeData>>,

    #[account(
        mut,
        seeds = [wormhole::FeeCollector::SEED_PREFIX],
        bump,
        seeds::program = wormhole_program.key,
    )]
    pub wormhole_fee_collector: Box<Account<'info, wormhole::FeeCollector>>,

    // ...

    #[account(
        mut,
        seeds = [
            wormhole::SequenceTracker::SEED_PREFIX,
            wormhole_emitter.key().as_ref(),
        ],
        bump,
        seeds::program = wormhole_program.key,
    )]
    pub wormhole_sequence: UncheckedAccount<'info>,
```

The instruction does not permit arbitrary reconfiguration of Wormhole router accounts. Instead, it only allows the owner to resynchronize `config.wormhole` with the `canonical bridge, fee_collector, and sequence addresses` derived for the program’s bound Wormhole deployment and the mint-specific emitter.

```rust
pub fn handler(ctx: Context<UpdateWormholeAccounts>) -> Result<()> {
    let bridge = ctx.accounts.wormhole_bridge.key();
    let fee_collector = ctx.accounts.wormhole_fee_collector.key();
    let sequence = ctx.accounts.wormhole_sequence.key();

    let old = ctx.accounts.config.wormhole.clone();

    require!(
        old.bridge != bridge || old.fee_collector != fee_collector || old.sequence != sequence,
        BridgeError::WormholeAccountsUnchanged,
    );
```

The handler also rejects no-op updates when the stored values already match the constrained accounts.

```rust
    require!(
        old.bridge != bridge || old.fee_collector != fee_collector || old.sequence != sequence,
        BridgeError::WormholeAccountsUnchanged,
    );
```


**Impact:** In the current implementation, `update_wormhole_accounts` is primarily a constrained recovery mechanism for correcting stale or inconsistent Wormhole account references in config. It may also serve as part of a migration flow only if accompanied by a bridge-program upgrade that changes the bound Wormhole deployment.

**Recommended Mitigation:** Document that `update_wormhole_accounts` is intended for recovery of canonical Wormhole account references, and not for routine reconfiguration.

**Securitize:** Updated documentation at [9e4cce](https://github.com/securitize-io/bc-solana-bridge-sc/commit/9e4cce95e654fb6c48191e36479da16414d7b1f2).

Acknowledged. The constraint is intentional - wormhole_bridge, wormhole_fee_collector, and wormhole_sequence are Anchor-constrained to the canonical PDAs derived from the bound wormhole_program and mint-specific wormhole_emitter, so update_wormhole_accounts can only resynchronize config.wormhole with those canonical addresses - it is not a free-form reconfiguration mechanism. The admin-instruction table in SECURITIZE_BRIDGE_SPECIFICATION.md has been reworded to state this explicitly, and a matching doc-comment has been added to the instruction handler.
