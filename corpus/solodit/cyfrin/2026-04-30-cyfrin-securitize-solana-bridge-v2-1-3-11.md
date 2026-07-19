---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-11
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`bridge_ds_tokens lamport` pre-check excludes additional rent costs'
vuln_class: []
---

# `bridge_ds_tokens lamport` pre-check excludes additional rent costs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The `bridge_ds_tokens` handler requires the payer’s SOL balance to be at least `wormhole_bridge.fee() + exec_amount` before any CPIs.


```rust
    let fee = ctx.accounts.wormhole_bridge.fee();

    // Require payer has enough lamports to cover fees
    require_gte!(
        ctx.accounts.payer.lamports(),
        fee.saturating_add(exec_amount),
        BridgeError::InsufficientLamportsForFees,
    );
```

Subsequent steps, in order, are:

1. Optional system transfer of `fee` from payer to `wormhole_fee_collector` (when `fee > 0`).
2. Wormhole `post_message` CPI with `payer` as a writable signer—this typically funds creation/rent for the posted message account and is **not** represented in `fee + exec_amount` above.

```rust
    if fee > 0 {
        invoke_wormhole_fee_transfer_cpi(&ctx, fee)?;
    }

    // ... payload encoding ...

    let sequence = invoke_post_message_cpi(
        &ctx,
        payload_bytes,
        outgoing_sequence,
        wormhole_message_bump,
    )?;

    // Request execution via the Wormhole Executor program.
    invoke_request_execution_cpi(
        &ctx,
        sequence,
        target_chain,
        exec_amount,
        signed_quote_bytes,
    )?;
```

The Wormhole SDK also wires `post_message` with the payer as a mutable account:

```rust
#[derive(Accounts)]
pub struct PostMessage<'info> {
    pub config: AccountInfo<'info>,
    pub message: AccountInfo<'info>,
    pub emitter: AccountInfo<'info>,
    pub sequence: AccountInfo<'info>,
    pub payer: AccountInfo<'info>,
    pub fee_collector: AccountInfo<'info>,
    pub clock: AccountInfo<'info>,
    pub rent: AccountInfo<'info>,
    pub system_program: AccountInfo<'info>,
}
```

Thus, a successful end-to-end execution may require additional lamports beyond those two values. In particular, the subsequent Wormhole post_message CPI uses the payer as a mutable funding account and may require extra lamports for message-account rent or related account creation costs.

As a result, this check should not be interpreted as a complete on-chain minimum-balance invariant for a successful bridge transaction. A payer may satisfy the bridge’s explicit pre-check and still fail later during downstream CPI execution due to insufficient lamports for ren

**Impact:** Wallets and integrators lack an on-chain **single** minimum-SOL invariant must infer extra headroom for Wormhole message rent and account rent-exempt minimums off-chain.

**Recommended Mitigation:** Document a recommended SOL buffer above `fee + exec_amount` that accounts for posted-message rent (first vs subsequent posts may differ) and payer rent-exempt minimum after debits.

**Securitize:** Updated doc at [0af5f26](https://github.com/securitize-io/bc-solana-bridge-sc/commit/0af5f2611c398560489a2680481605e604cd36b1).

Acknowledged. Documentation updated to specify a recommended SOL buffer of ≥ 0.01 SOL above wormhole_fee + exec_amount, with the full formula and rent derivation in the bridge specification and the SDK README.
