---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: On-Ramp `initialize` Should Reject Zero Genesis Hash
vuln_class: []
---

# On-Ramp `initialize` Should Reject Zero Genesis Hash

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** The on-ramp `initialize` instruction uses `[0; 32]` as the sentinel for “genesis hash PDA not yet set” but does not reject the same value when it is passed as the `genesis_hash` instruction argument.

```rust
    // Genesis hash is a singleton config used for signature domain separation.
    // It is set once on first initialize; subsequent initializes must match.
    if ctx.accounts.genesis_hash.hash == [0; 32] {
        ctx.accounts.genesis_hash.set_inner(GenesisHash {
            hash: genesis_hash,
            bump: ctx.bumps.genesis_hash,
        });
    } else {
        require!(
            ctx.accounts.genesis_hash.hash == genesis_hash,
            crate::errors::SecuritizeOnRampError::GenesisHashMismatch
        );
    }
```

There is no upfront check that the **instruction argument** `genesis_hash != [0; 32]`, so the “wrong” outcome (storing zero) is not prevented.

```rust
pub fn initialize_handler(
    ctx: &mut Context<Initialize>,
    fee_manager: crate::FeeManager,
    asset_provider: crate::AssetProvider,
    nav_provider: crate::NavProvider,
    custodian_wallet: Pubkey,
    genesis_hash: [u8; 32],
) -> Result<()> {
```

As a result, the first `initializer` can set the singleton genesis hash to an all-zero value. This value is then used as the cluster-specific domain separator for signature verification (e.g., in `swap_spl_token`). Moreover, this design does not guarantee that the `genesis_hash` remains consistent across all on-ramp states.

**Impact:** Failing to reserve `[0; 32]` as “uninitialized only” blurs the meaning of the sentinel.

**Recommended Mitigation:** Reject the zero hash at the start of the handler so it is reserved for “uninitialized” only and cannot be stored as the genesis hash.

**Securitize:** Fixed in [5b035d1](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/5b036d1a53e59a2a9c7d59a43bb98195e6240517).

**Cyfrin:** Verified.
