---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: Outbound DS/SPL bridge handlers do not validate EVM recipient address format
vuln_class: []
---

# Outbound DS/SPL bridge handlers do not validate EVM recipient address format

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** The DS and SPL outbound bridge instructions (`bridge_ds_tokens` and `bridge_spl_tokens`) accept any non-zero 32-byte `recipient`, without verifying that it is a well-formed EVM address for the target chain.

Both outbound DS and SPL handlers delegate recipient validation to the shared helper `check_bridge_send_args`, which only rejects the zero address and positive-amount checks:

```16:36:bc-solana-bridge-sc/programs/securitize_bridge/src/utils/bridge_send/checks.rs
pub fn check_bridge_send_args(
    asset_mint: &Pubkey,
    target_chain: u16,
    recipient: &[u8; 32],
    amount: u64,
) -> Result<()> {
    require_keys_neq!(*asset_mint, ZERO_PUBKEY, BridgeError::ZeroAssetMint);

    #[cfg(not(feature = "devnet"))]
    require!(
        target_chain != wormhole::CHAIN_ID_SOLANA,
        BridgeError::CannotBridgeToSameChain,
    );
    #[cfg(feature = "devnet")]
    let _ = target_chain;

    require!(*recipient != ZERO_ADDRESS, BridgeError::InvalidRecipient);

    require_gt!(amount, 0, BridgeError::InvalidBridgeAmount);

    Ok(())
}
```

`bridge_ds_tokens` and `bridge_spl_tokens` both call this helper before burning/revoking tokens and posting the Wormhole message:

```213:213:bc-solana-bridge-sc/programs/securitize_bridge/src/instructions/bridge/bridge_ds_tokens.rs
    check_bridge_send_args(&config.asset_mint, target_chain, &recipient, amount)?;
```

```164:164:bc-solana-bridge-sc/programs/securitize_bridge/src/instructions/bridge/bridge_spl_tokens.rs
    check_bridge_send_args(&config.asset_mint, target_chain, &recipient, amount)?;
```

The encoded payload stores the caller-supplied `recipient` verbatim as `destination_wallet`:

```193:202:bc-solana-bridge-sc/programs/securitize_bridge/src/instructions/bridge/bridge_spl_tokens.rs
    let payload_bytes = abi_encode_bridge_payload(&BridgePayload {
        target_chain,
        investor_id: investor_id.clone(),
        value: amount,
        investor_wallet: ctx.accounts.payer.key().to_bytes(),
        destination_wallet: recipient,
        country: String::new(),
        attribute_values: vec![0u64; 4],
        attribute_expirations: vec![0i64; 4],
    })?;
```

By contrast, the USDC bridge outbound handler applies an additional EVM-format check on the same 32-byte field:

```173:180:bc-solana-bridge-sc/programs/securitize_usdc_bridge/src/instructions/bridge/send_usdc_cross_chain_deposit.rs
    require_gt!(amount, 0, UsdcBridgeError::InvalidAmount);
    require!(recipient != ZERO_ADDRESS, UsdcBridgeError::InvalidRecipient);

    // A valid EVM address in 32-byte form must be left-padded with 12 zero bytes
    require!(
        recipient[..12] == [0u8; 12],
        UsdcBridgeError::InvalidEvmAddress,
    );
```

**Impact:** A user (or integrator) may pass a raw Solana pubkey, an unpadded hex string, or another malformed 32-byte value as the destination.

**Recommended Mitigation:** Align DS/SPL outbound validation with the USDC bridge.

**Securitize:** Fixed in commit [d7e9ba1f128](https://github.com/securitize-io/bc-solana-bridge-sc/commit/d7e9ba1f128fa860571b8c6acad55b3a39ab3d7f). The shared check_bridge_send_args helper (used by both bridge_ds_tokens and bridge_spl_tokens) now enforces the EVM-address format on the 32-byte recipient, aligning DS/SPL outbound with the USDC bridge: it requires the high 12 bytes to be zero (recipient[..12] == [0u8; 12], else InvalidEvmAddress).

**Cyfrin:** Verified.
