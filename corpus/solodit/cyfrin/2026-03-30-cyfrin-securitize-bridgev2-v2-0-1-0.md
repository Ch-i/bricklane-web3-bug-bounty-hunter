---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-30-cyfrin-securitize-bridgev2-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-bridgev2-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-30-cyfrin-securitize-bridgev2-v2-0
title: Permanent loss of DSTokens when bridging to non-EVM chains via the backward-compatible
  `SecuritizeBridge::bridgeDSTokens` due to missing target chain type validation
vuln_class: []
---

# Permanent loss of DSTokens when bridging to non-EVM chains via the backward-compatible `SecuritizeBridge::bridgeDSTokens` due to missing target chain type validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-30-cyfrin-securitize-bridgev2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-bridgev2-v2.0.md)_

---

**Description:** `SecuritizeBridge.bridgeDSTokens(uint16 _targetChain, uint256 _value)` is the backward-compatible bridge entry point for users who want to bridge DS tokens to the same wallet address on a destination chain. To derive the destination address, it encodes `msg.sender` (a 20-byte EVM address) into a 32-byte value using EVM-specific padding:

```solidity
// SecuritizeBridge.bridgeDSTokens(uint16 _targetChain, uint256 _value)
bytes32 destinationAddress = bytes32(uint256(uint160(_msgSender())));
```

This encoding is only valid for EVM-compatible chains (Ethereum, Arbitrum, Avalanche, Base, Optimism, Polygon), where addresses are 20 bytes padded to 32. Non-EVM chains supported by the bridge — specifically Solana (Wormhole chain ID 1) — use a different address scheme: Ed25519 public keys, which are natively 32 random bytes and bear no structural relationship to EVM addresses.

If a user calls the backward-compatible `SecuritizeBridge::bridgeDSTokens` and it passes the `_targetChain` as the ID of a non-EVM chain, the burnt bridged tokens are permanently unrecoverable.

The precondition is a user calling `SecuritizeBridge::bridgeDSTokens` — the simpler, backward-compatible entry point — with a non-EVM target chain ID. Unlike `SecuritizeBridge.bridgeDSTokensToAddress(uint16 _targetChain, uint256 _value, bytes32 _destinationAddress)`, which requires callers to supply a chain-appropriate bytes32 destination and is therefore more explicitly a power-user interface.

The call path is:

1. `bridgeDSTokens(_targetChain=1, _value)` — encodes `msg.sender` as `bytes32(uint256(uint160(msg.sender)))` (EVM padding)
2. Calls `bridgeDSTokensToAddress(1, _value, malformedBytes32)` — no zero-check or chain-type check
3. `_bridgeDSTokensInternal()` — validates investor compliance, burns tokens, publishes VAA with malformed destination
4. Executor delivers VAA to Solana bridge
5. Solana bridge issues tokens to the 32-byte value — an address the user does not own

No validation between steps 1 and 2 checks whether `_targetChain` corresponds to an EVM chain before applying EVM-specific address encoding.

**Recommended Mitigation:** Add a check in `SecuritizeBridge::bridgeDSTokens` that reverts if `_targetChain` is not an EVM-compatible chain before deriving the destination address from `msg.sender`. Maintain an allowlist of EVM Wormhole chain IDs (or a mapping of chain ID to address type), and revert with a descriptive error when a non-EVM chain ID is supplied to the backward-compatible entry point.

**Securitize:** Fixed in commit [328f890](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/328f890f5726ce2aec8b2ab7a55ef455784a4586).

**Cyfrin:** Verified. Added a check in `SecuritizeBridge::bridgeDSTokens`  to revert if `_targetChain` is not an EVM-compatible chain.

\clearpage
