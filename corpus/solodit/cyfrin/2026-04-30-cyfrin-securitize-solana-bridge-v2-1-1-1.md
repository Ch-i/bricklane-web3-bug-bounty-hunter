---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Inbound Transfers Mint Against Stale Destination Identity State Bypassing Jurisdiction-Specific
  Lock Periods
vuln_class: []
---

# Inbound Transfers Mint Against Stale Destination Identity State Bypassing Jurisdiction-Specific Lock Periods

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The bridge payload carries investor compliance metadata -- country and attribute values/expirations -- but this data is conditionally omitted by the EVM sender and unconditionally ignored by the Solana receiver. The result is that tokens can be minted on the destination chain using whatever identity state was last written there, even if the source chain's current state is more restrictive.

On the EVM send side, `_encodePayload` only includes the full investor detail (country, attributes) when the source and destination wallets are identical. When they differ, it sends empty strings and empty arrays:

```solidity
// SecuritizeBridge.sol
function _encodePayload(...) private pure returns (bytes memory) {
    if (_isSameWallet) {
        return abi.encode(
            _targetChain,
            _investorDetail.investorId,
            _value,
            _sourceWallet,
            _destinationAddress,
            _investorDetail.country,
            _investorDetail.attributeValues,
            _investorDetail.attributeExpirations
        );
    }
    return abi.encode(
        _targetChain,
        _investorId,
        _value,
        _sourceWallet,
        _destinationAddress,
        "",
        new uint256[](0),
        new uint256[](0)
    );
}
```

For EVM-to-Solana transfers, the wallets can never match -- one is an EVM address (`bytes32`-padded `address`) and the other is a Solana `Pubkey`. So this code path *always* strips compliance metadata from cross-chain transfers to Solana.

On the Solana receive side, `execute_vaa_v1` decodes the payload but only uses three fields from it: `target_chain`, `destination_wallet`, and `investor_id`. It does not read or apply `country`, `attribute_values`, or `attribute_expirations` at all:

```rust
// execute_vaa_v1.rs
let decoded_payload =
    abi_decode_bridge_payload(&payload_bytes).ok_or(error!(BridgeError::InvalidPayload))?;

require!(
    decoded_payload.target_chain == wormhole::CHAIN_ID_SOLANA,
    BridgeError::CannotBridgeToSameChain,
);

// ...

require!(
    ctx.accounts.recipient_wallet.key() == destination_wallet,
    BridgeError::RecipientMismatch,
);

require!(
    ctx.accounts.investor.investor_id == decoded_payload.investor_id,
    BridgeError::InvestorIdMismatch,
);

// Immediately issues tokens -- no identity state update
invoke_issue_tokens_cpi(...)?;
```

The minted tokens then become subject to Solana's outbound lock validation, which reads the investor's `country` from the *local* `IdentityAccount` on Solana to determine the applicable lock period:

```rust
// bridge_ds_tokens.rs
let identity =
    IdentityAccount::deserialize_checked(&ctx.accounts.identity_account.to_account_info())?;

locked_tokens::validate_locked_tokens(
    &ctx.accounts.tracker_account.to_account_info(),
    &ctx.accounts.policy_engine.to_account_info(),
    identity.country,  // <-- stale local value
    balance,
    amount,
    ctx.accounts.clock.unix_timestamp,
)?;
```

```rust
// locked_tokens.rs
let region = policy_engine.mapping[investor_country as usize];

let lock_period = if region == REGION_US {
    policy_engine.issuance_policies.us_lock_period
} else {
    policy_engine.issuance_policies.non_us_lock_period
};
```

The lock period selection is binary: US investors get `us_lock_period`, everyone else gets `non_us_lock_period`. If the local Solana identity says "non-US" but the investor's actual status on the EVM source chain was updated to "US", the shorter non-US lock period applies.

The EVM receive side has a symmetric gap. For different-wallet inbound transfers, it skips `updateInvestor` entirely and only checks that the destination wallet is already registered to the correct investor:

```solidity
// SecuritizeBridge.sol - executeVAAv1
if (sourceWallet == destinationAddress) {
    registryService.updateInvestor(investorId, investorId, country,
        investorWallets, attributeIds, attributeValues, attributeExpirations);
} else {
    bool isDestinationRegistered = registryService.isWallet(destinationWallet);
    // ... only checks wallet ownership, no identity update
}

_dsToken.issueTokens(destinationWallet, value);
```

**Impact:** An investor whose compliance status changes on one chain can bridge tokens to the other chain where the stale, more permissive status still applies. The concrete consequence is lock period evasion:

1. Investor is registered as non-US on Solana (shorter or zero lock period).
2. Investor's jurisdiction changes to US on the EVM side.
3. Investor bridges EVM -> Solana. The payload omits country (different wallets). Solana mints without updating the identity.
4. Investor immediately bridges the newly minted tokens out from Solana. The lock validation reads the stale non-US country code and applies the shorter lock period instead of the US lock period.

The same pattern applies to attribute expirations. If KYC or accreditation expires on the source chain but remains unexpired in the stale destination record, the bridge effectively launders the compliance status.

**Proof of Concept:**
1. Register an investor on both Solana and EVM with country = non-US (e.g., country code 0 on Solana, `""` on EVM).
2. On the EVM side, update the investor's country to US via the registry service.
3. Bridge tokens from EVM to Solana. Because `sourceWallet != destinationAddress` (EVM address vs Solana pubkey), the payload contains `country: ""` and empty attributes.
4. Solana `execute_vaa_v1` mints tokens. It does not read or apply the (empty) country field. The local `IdentityAccount.country` remains 0 (non-US).
5. Immediately call `bridge_ds_tokens` on Solana to bridge outbound. The lock validation reads `identity.country = 0`, maps it to the non-US region, and applies `non_us_lock_period`.
6. The investor bypasses the US lock period that should have applied based on their current jurisdiction.

**Recommended Mitigation:** The bridge should synchronize compliance state on every inbound path, not just the same-wallet EVM path.

1. **Always include compliance metadata in the payload.** Remove the `isSameWallet` conditional in `_encodePayload`. Cross-format address differences (EVM vs Solana) make the same-wallet optimization structurally incompatible with cross-chain bridging.

2. **Apply incoming metadata on Solana receive.** `execute_vaa_v1` should update the local `IdentityAccount` country and attributes from the decoded payload before issuing tokens, or at minimum validate that the local state is not more permissive than the incoming state.

3. **Apply incoming metadata on EVM receive for different-wallet transfers.** The `else` branch in `executeVAAv1` should call `updateInvestor` (or a lighter-weight update) rather than skipping it entirely.

4. **If real-time sync is infeasible**, enforce a conservative fallback: apply the most restrictive lock period when compliance metadata is absent or empty, rather than trusting stale local state.


**Securitize:** Acknowledged as a known system-level assumption, not a bridge-specific bug.

On-chain investor identity (country, attributes, expirations) is treated as the authoritative source of truth for compliance decisions. Cross-chain identity consistency is an operational guarantee managed by the Securitize compliance team as part of a unified off-chain KYC process — investors are not registered with different jurisdictions or attribute sets on different chains.

This assumption is shared by every on-chain component that reads investor identity from the local registry. Stale identity on any chain would affect all such components equally, not only the bridge. A conservative fallback applied in the bridge alone (e.g. using the stricter lock period when payload metadata is absent) would duplicate responsibility already owned by the compliance layer and would not protect other components reading the same local identity data.
