---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-10
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
title: Inbound `execute_vaa_v1` does not validate posted VAA finality
vuln_class: []
---

# Inbound `execute_vaa_v1` does not validate posted VAA finality

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** After parsing the Wormhole posted VAA, the instruction checks:

- `posted.emitter_chain() == emitter_chain`
- `posted.sequence() == sequence`
- `emitter_address.verify(posted.emitter_address())`

but does not check `posted.finality()` before processing the payload and minting tokens.


```rust
    let posted_data = posted_account.try_borrow_data()?;
    let posted = wormhole::PostedVaaData::try_from_account_data(&posted_data)?;

    // Require posted VAA emitter chain matches emitter chain argument.
    require!(
        posted.emitter_chain() == emitter_chain,
        BridgeError::WrongEmitterChain,
    );

    // Require posted VAA sequence matches sequence argument.
    require!(posted.sequence() == sequence, BridgeError::WrongSequence,);

    // Require posted VAA emitter address matches registered peer for this source chain.
    require!(
        ctx.accounts
            .emitter_address
            .verify(posted.emitter_address()),
        BridgeError::WrongBridgeInitiator,
    );

    let payload_bytes = posted.payload.clone();
```

Outbound messages do use `BridgeConfig.finality` when calling `wormhole::post_message`, so the bridge already has a configured finality parameter on the send side. That parameter is not enforced on the receive side.


**Impact:** The issue is that inbound redemption does not enforce any minimum finality threshold locally. If trusted remote peers emit messages at a lower consistency level than expected, Solana will still accept and execute them.

**Recommended Mitigation:** If a minimum inbound consistency level is part of the intended bridge policy, enforce it explicitly in `execute_vaa_v1` by validating `posted.finality()`.

**Securitize:** Fixed in [0a36d25](https://github.com/securitize-io/bc-solana-bridge-sc/commit/0a36d2571d1fcc4b3a074711ff45f088f07cf5fe), [e1f63329](https://github.com/securitize-io/bc-solana-bridge-sc/commit/e1f63329eb94bf2dc70f91b7f933bae49cd95c9f) and [9dc1166](https://github.com/securitize-io/bc-solana-bridge-sc/commit/9dc11664d3e6c2eaf024c6e6627707365a2fd11f).

- Added a `posted.finality() == Finalized` check with a new `InsufficientFinality` error in `execute_vaa_v1`, rejecting inbound VAAs that the source chain did not attest as finalized.
- Removed the `min_consistency_level != 0` validation in `set_emitter_address`.
- Changed the inbound check in `execute_vaa_v1 from == to >= against EmitterAddress.min_consistency_level`. The field name implies a minimum, and >= correctly accepts stronger consistency levels.


**Cyfrin:** Verified.
