---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: '`SecuritizeBridge::executeVAAv1` VAA payload omits destination-contract binding,
  enabling cross-instance double-mint across co-deployed bridge instances on one chain'
vuln_class: []
---

# `SecuritizeBridge::executeVAAv1` VAA payload omits destination-contract binding, enabling cross-instance double-mint across co-deployed bridge instances on one chain

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** The Wormhole VAA payload encodes `targetChain` (a chain-level Wormhole chain ID) but does not include the address of the destination `SecuritizeBridge` contract. `executeVAAv1` validates the source emitter (`emitterAddresses[sourceChain]`, `contracts/bridge/SecuritizeBridge.sol:338-340`), confirms `targetChain == _wormholeCore.chainId()` (`contracts/bridge/SecuritizeBridge.sol:355`), and guards against replay via `isVaaConsumed[vm.hash]` (`contracts/bridge/SecuritizeBridge.sol:358-359`) - but `isVaaConsumed` is per-proxy storage.

Nothing in the signed payload or in the verification logic binds a given VAA to one specific `SecuritizeBridge` instance. If two `SecuritizeBridge` proxies are deployed on the same destination chain - for example, a v2 deployment running alongside a legacy instance, or one bridge per DS token series - and both register the same source emitter via `setEmitterAddress`, a single source-chain burn produces one VAA that each instance independently accepts. Each proxy holds its own `isVaaConsumed` mapping, so the replay guard is satisfied independently on both, and `issueTokens` is called on each proxy's configured `dsToken` for the full bridged `value`.

**Files:**

`SecuritizeBridge::executeVAAv1, _encodePayload`

**Impact:** A single source burn can yield two destination issuances - one per co-deployed bridge instance sharing the same emitter configuration. The supply-conservation constraint that every investor must not receive more tokens on the destination than were burned on the source is broken for any deployment topology where two instances share an emitter on the same destination chain. The protocol currently provides no code-level defense against this topology, and `setEmitterAddress` does not enforce emitter uniqueness across bridge instances.

**Recommended Mitigation:** Bind the VAA to the specific destination bridge instance inside the guardian-signed payload. At the source, `_bridgeDSTokensInternal` already knows the configured destination via `bridgeAddresses[_targetChain]`; encode THAT value (not `address(this)`) as a destination-binding field in `SecuritizeBridge::_encodePayload` (`contracts/bridge/SecuritizeBridge.sol:503`), and in `executeVAAv1` decode it and require it equals `_addressToBytes32(address(this))` before consuming the replay slot.

Note that `address(this)` evaluated inside `_encodePayload` is the SOURCE bridge, not the destination, so encoding `address(this)` there would not bind the destination instance. A purely local extended replay key such as `(vm.hash, address(this))` is also insufficient, because the destination-contract identity must live inside the signed VAA body, not just in a local check.

**Securitize:** Acknowledged for now as this is a payload-breaking change and it is unlikely in practice for multiple `SecuritizeBridge` instances to be deployed on the same chain.
