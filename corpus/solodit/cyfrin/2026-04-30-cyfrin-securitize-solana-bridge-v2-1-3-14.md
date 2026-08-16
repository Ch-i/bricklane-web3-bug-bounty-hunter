---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-14
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: USDCBridgeSend does not expose a direct CCTP correlation identifier
vuln_class: []
---

# USDCBridgeSend does not expose a direct CCTP correlation identifier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `USDCBridgeSend` intentionally emits only bridge-level fields (`bridge_instance, target_chain_id, recipient, amount`). While the transaction also includes Circle CCTP CPI execution and a dedicated `cctp_message_sent_event_data` account, the custom bridge event itself is not sufficient as a standalone correlation record for downstream indexers that want to map bridge sends directly to Circle message identifiers.

```rust
#[event]
pub struct USDCBridgeSend {
    /// USDC bridge config PDA (`[config, usdc_mint]`) identifying this bridge deployment.
    pub bridge_instance: Pubkey,
    pub target_chain_id: u16,
    pub recipient: [u8; 32],
    pub amount: u64,
}
```


The handler emits it **after** `invoke_deposit_for_burn` and executor fee logic, still without any CCTP message identifier:

```196:211:programs/securitize_usdc_bridge/src/instructions/bridge/send_usdc_cross_chain_deposit.rs
    invoke_deposit_for_burn(&ctx, destination_domain, amount, recipient)?;

    {
        validate_payer_lamports_for_executor(&ctx, exec_amount)?;
        invoke_request_execution_cpi(&ctx, target_chain, exec_amount, signed_quote_bytes)?;
        reimburse_executor_fee(&ctx, exec_amount)?;
    }

    emit_cpi!(USDCBridgeSend {
        bridge_instance: ctx.accounts.config.key(),
        target_chain_id: target_chain,
        recipient,
        amount,
    });
```

**Impact:** Harder **end-to-end tracing** from “user bridged on Solana” to “specific CCTP message / attestation / mint on destination” using only `USDCBridgeSend`.

**Recommended Mitigation:** After `deposit_for_burn`, if the program can **deterministically read** the emitted nonce and message hash from documented Circle account layouts or CPI return data for the supported Message Transmitter version, **extend `USDCBridgeSend`** (or add a companion event) with `nonce` and `message_hash` (or a single `message_id`/`guid` if that is the stable external identifier).

**Securitize:** Thanks for the observation. We acknowledge this is informational and intend to leave the event shape unchanged for the following reasons:

Circle CCTP V2 emits its own MessageSent CPI event in the same transaction via the cctp_event_authority, containing the authoritative nonce and full message bytes (from which message_hash is derived). This is the canonical correlation source and is already consumed by standard CCTP indexers.

The cctp_message_sent_event_data account is present as a named account in our instruction, so off-chain indexers can trivially locate and decode it from the transaction.

Our USDCBridgeSend event and Circle's MessageSent event share the same transaction signature, which is a sufficient and stable correlation key.

Extending USDCBridgeSend with nonce / message_hash would require our program to deserialize Circle's internal MessageSent account layout or re-hash the raw message bytes after CPI. Both couple us to Circle's private V2 encoding, which we consider a larger long-term risk than the minor indexer convenience gained.
