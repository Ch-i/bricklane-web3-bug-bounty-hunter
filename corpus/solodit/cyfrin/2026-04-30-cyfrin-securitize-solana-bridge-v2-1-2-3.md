---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-3
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
title: Outbound Payload Encoding Uses `panic!` Instead of Anchor Error Codes
vuln_class: []
---

# Outbound Payload Encoding Uses `panic!` Instead of Anchor Error Codes

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `abi_encode_bridge_payload` in `modules/securitize-bridge-core/src/payload.rs:174-209` validates its input by calling `panic_for_invalid_bridge_payload`, which converts every `PayloadError` variant into a `panic!`:

```rust
// payload.rs:128-145
#[cfg(feature = "abi")]
fn panic_for_invalid_bridge_payload(payload: &BridgePayload) {
    match validate_bridge_payload(payload) {
        Ok(()) => {}
        Err(PayloadError::AttributeLengthMismatch) => {
            panic!("attribute_values and attribute_expirations must have the same length")
        }
        Err(PayloadError::InvalidAttributeCount) => {
            panic!("Bridge payload requires exactly 4 attributes ...")
        }
        Err(PayloadError::InvestorIdTooLong) => {
            panic!("investor_id length exceeds max {}", MAX_INVESTOR_ID_LEN)
        }
        Err(PayloadError::CountryTooLong) => {
            panic!("country length exceeds max {}", MAX_COUNTRY_LEN)
        }
        Err(other) => panic!("unexpected payload validation error: {other:?}"),
    }
}
```

A second raw `assert!` guards the final encoded length:

```rust
// payload.rs:202-206
assert!(
    encoded_payload_fits_max_len(encoded.len()).is_ok(),
    "encoded payload exceeds max length {}",
    MAX_ENCODED_PAYLOAD_LENGTH
);
```

On Solana, `panic!` produces an opaque `ProgramError` with no Anchor error code, no discriminator, and no structured log. The runtime returns a generic instruction-failure code to the caller.

This function is called during the outbound bridge flow in `programs/securitize_bridge/src/instructions/bridge/bridge_ds_tokens.rs:325`. Of the validation checks, the `investor_id` length is the most externally reachable: the value comes from an external `ImrInvestor` account and is not length-bounded by the bridge program. If an investor's `investor_id` exceeds `MAX_INVESTOR_ID_LEN` (256 bytes), `panic_for_invalid_bridge_payload` fires, permanently blocking that investor from outbound bridging with an uninformative error.

The remaining checks (attribute count, country length, encoded payload size) are internally bounded by program logic and unlikely to fire in practice, but they follow the same panic pattern.

Notably, the codebase already defines proper `PayloadError` variants (`InvestorIdTooLong`, `CountryTooLong`, `InvalidAttributeCount`, etc.) and structured validation functions (`validate_bridge_payload`, `validate_payload_lengths`) that return `Result<(), PayloadError>`. These are used by the decode path but bypassed on the encode path, which wraps them in panics instead of propagating them.

**Recommended Mitigation:** Have `abi_encode_bridge_payload` return `Result<Vec<u8>, PayloadError>` instead of `Vec<u8>`, propagating the existing structured error types. At the call site in `bridge_ds_tokens.rs`, map `PayloadError` variants to `BridgeError` variants via `require!` or a `.map_err()`:

```rust
// payload.rs
pub fn abi_encode_bridge_payload(payload: &BridgePayload) -> Result<Vec<u8>, PayloadError> {
    validate_bridge_payload(payload)?;

    // ... encoding logic ...

    encoded_payload_fits_max_len(encoded.len())?;
    Ok(encoded)
}
```

```rust
// bridge_ds_tokens.rs
let payload_bytes = abi_encode_bridge_payload(&BridgePayload { ... })
    .map_err(|_| BridgeError::InvalidPayload)?;
```

**Securitize:** Fixed in [4a916d4](https://github.com/securitize-io/bc-solana-bridge-sc/commit/4a916d4658e5bf56f862ddaaec8a35eb71928939).

**Cyfrin:** Verified.
