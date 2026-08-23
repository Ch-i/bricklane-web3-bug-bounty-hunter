---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Bridge initializes Wormhole outbound messages with `Confirmed` finality by
  default, weakening reorg safety
vuln_class: []
---

# Bridge initializes Wormhole outbound messages with `Confirmed` finality by default, weakening reorg safety

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** New bridge instances initialize `config.finality` to `wormhole::Finality::Confirmed` in `initialize.rs`

```rust
    config.wormhole.bridge = ctx.accounts.wormhole_bridge.key();
    config.wormhole.fee_collector = ctx.accounts.wormhole_fee_collector.key();
    config.wormhole.sequence = ctx.accounts.wormhole_sequence.key();
    config.batch_id = 0;
    config.finality = wormhole::Finality::Confirmed as u8;
    config.paused = false;
```

And outbound transfers pass this value directly to Wormhole `post_message` in `bridge_ds_tokens`.
```rust
    let finality =
        wormhole::Finality::try_from(config.finality).map_err(|_| BridgeError::InvalidMessage)?;

    wormhole::post_message(post_message_ctx, config.batch_id, payload_bytes, finality)?;
```


On Solana, `Confirmed` provides weaker reorg resistance than `Finalized`, so guardians may attest to messages before the source-chain burn has the strongest available settlement assurances. Although the owner can later update the setting via `update_finality`, newly initialized bridge instances remain on the weaker default unless operators explicitly change it.


**Impact:** In an adverse reorg scenario, a VAA could be produced and redeemed on the destination chain while the originating Solana burn is later excluded from finalized history, creating a temporary or permanent
  cross-chain supply accounting inconsistency.

**Recommended Mitigation:** Default new bridge configurations to `wormhole::Finality::Finalized`.

**Securitize:** Fixed in [ef38bd](https://github.com/securitize-io/bc-solana-bridge-sc/commit/ef38bd108626f1582bbe15cc15e60b0fb644fd85).

**Cyfrin:** Verified.
