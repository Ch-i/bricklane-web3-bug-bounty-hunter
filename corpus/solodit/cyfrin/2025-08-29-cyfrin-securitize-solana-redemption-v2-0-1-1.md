---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-securitize-solana-redemption-v2-0-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-securitize-solana-redemption-v2-0
title: Permissionless OffRampState initialization under official program ID enables
  spoofed “official” instances
vuln_class: []
---

# Permissionless OffRampState initialization under official program ID enables spoofed “official” instances

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md)_

---

**Description:** The `initialize` instruction lets any signer create a new `OffRampState` and become its `admin`. The global `OffRampCounter` is `init_if_needed` and unguarded, and the new state PDA is derived from `[OFF_RAMP_STATE_SEED, off_ramp_counter.counter.to_le_bytes()]`. There is no allowlist or registry check tying the initializer to an official Securitize operator.
This means anyone can spin up an OffRamp instance under the same Program ID and emit an `Initialized` event, which can be marketed as if it were an official, Securitize backed off ramp.
```rust
/// Global counter for generating unique off-ramp IDs
#[account(
    init_if_needed,
    payer = admin,
    space = 8 + OffRampCounter::INIT_SPACE,
    seeds = [OFF_RAMP_COUNTER_SEED],
    bump,
)]
pub off_ramp_counter: Box<Account<'info, OffRampCounter>>,

/// Off-ramp state containing configuration and settings
#[account(
    init,
    payer = admin,
    space = 8 + OffRampState::INIT_SPACE,
    seeds = [OFF_RAMP_STATE_SEED, off_ramp_counter.counter.to_le_bytes().as_ref()],
    bump,
)]
pub off_ramp_state: Box<Account<'info, OffRampState>>,
```

**Impact:** A third party can deploy a look alike instance with arbitrary fees, NAV provider, and recipient policy, then present it as “the Securitize off ramp” because it is hosted under the same Program ID.


**Recommended Mitigation:** Add a `GlobalConfig` PDA that stores an `authorized_initializer` or allowlist. In `initialize`, require the `admin` signer to be on that list.

**Securitize:** Fixed in [30362cf](https://github.com/securitize-io/bc-solana-redemption-sc/commit/30362cf3d6b349cad72134f843808464d7477502).

**Cyfrin:** Verified.


\clearpage
