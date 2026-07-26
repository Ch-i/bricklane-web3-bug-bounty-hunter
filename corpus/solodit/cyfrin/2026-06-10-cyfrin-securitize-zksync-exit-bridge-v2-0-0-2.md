---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-0-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: '`ZKSyncSecuritizeBridge::bridgeDSTokens` hard-binds the Ethereum mint destination
  to `msg.sender` with no escape hatch for ZKSync smart-contract wallets'
vuln_class: []
---

# `ZKSyncSecuritizeBridge::bridgeDSTokens` hard-binds the Ethereum mint destination to `msg.sender` with no escape hatch for ZKSync smart-contract wallets

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** `ZKSyncSecuritizeBridge::bridgeDSTokens` constructs both `sourceWallet` and `destinationAddress` from `msg.sender` via `_addressToBytes32(_msgSender())` (`contracts/bridge/ZKSyncSecuritizeBridge.sol:129`), enforcing `sourceWallet == destinationAddress` at the contract level. The companion function `bridgeDSTokensToAddress` is disabled with a `NotImplemented` revert (`contracts/bridge/ZKSyncSecuritizeBridge.sol:88`), eliminating any alternate-destination path.

ZKSync Era uses a different CREATE2 derivation for smart-contract wallets than Ethereum mainnet: a contract wallet address computed on ZKSync is not controlled by the same bytecode at the same address on Ethereum, unless the deployer has taken explicit steps to ensure address parity. This is more relevant on ZKsync than a typical chain because ZKsync has native account abstraction - smart-contract accounts are a first-class, common wallet type there, not an edge case.

An investor using a smart-contract wallet (a multisig, an account-abstraction wallet, or a proxy) on ZKSync that has not been identically reproduced on Ethereum cannot bridge their tokens: the minted tokens would go to an Ethereum address they do not control, and there is no code-level escape hatch to redirect the mint to an Ethereum address they do own.

**Files:**

`ZKSyncSecuritizeBridge::bridgeDSTokens, bridgeDSTokensToAddress`

**Impact:** Smart-contract wallet holders on ZKSync have no on-chain path to bridge their DS tokens to an Ethereum address they control. The tokens are burned on ZKSync and the off-chain Kafka relay would attempt to mint to an address they cannot sign for on Ethereum, effectively stranding the bridged value.

**Recommended Mitigation:** Enable an alternate-destination path on `ZKSyncSecuritizeBridge::bridgeDSTokensToAddress` (`contracts/bridge/ZKSyncSecuritizeBridge.sol:88`) subject to the same registration and compliance gate required by the Wormhole-based `SecuritizeBridge` different-wallet path.

Alternatively, document the smart-contract wallet limitation prominently so investors can verify address controllability before bridging. If the protocol wishes to continue prohibiting cross-wallet bridging, it should expose a pre-bridge address-parity check that reverts when the caller is a contract, allowing smart-contract wallet holders to learn of the limitation before their tokens are burned.

**Securitize:** Fixed in commit [`162f19d`](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/162f19d964d3fe1cda577d11a640f683b5bd1bcb)

**Cyfrin:** Verified. A `msg.sender` with `code.size > 0` is rejected hence preventing smart wallets from bridging.
