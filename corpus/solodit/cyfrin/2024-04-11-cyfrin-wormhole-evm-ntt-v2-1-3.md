---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Immutable gas limit within `WormholeTransceiver` can lead to execution failures
  on the target chain
vuln_class: []
---

# Immutable gas limit within `WormholeTransceiver` can lead to execution failures on the target chain

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** The Wormhole-specific Transceiver implementation uses an immutable [`gasLimit`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/Transceiver/WormholeTransceiver/WormholeTransceiverState.sol#L27) variable to calculate the Relayer delivery price. The underlying assumption here is that the gas consumed for transfers will always be static; however, this is not always the case, especially for L2 rollups such as Arbitrum, where gas is calculated as a function of the actual gas consumed on L2 and the L1 calldata cost that is effectively an L2 view of the L1 gas price. Please refer to the [Arbitrum docs](https://docs.arbitrum.io/inside-arbitrum-nitro#gas-and-fees) for more information on how gas is estimated.

In cases where L2 gas depends on the L1 gas price, extreme scenarios can occur where the delivery cost computed by the static gas limit is insufficient to execute a transfer on L2.

**Impact:** An immutable gas limit can give an extremely stale view of the L2 gas needed to execute a transfer. In extreme scenarios, such stale gas estimates can be insufficient to execute messages on a target chain. If such a scenario occurs, all pending messages with a stale gas estimate will risk being stuck on the target chain. While the gas limit can be changed via an upgrade, there are two issues with this approach:
1. Synchronizing a mass update across a large number of `NttManager` contracts might be difficult to execute.
2. Changing the gas limit has no impact on pending transfers that are already ready for execution on the target chain.

**Recommended Mitigation:** Consider making the gas limit mutable. If necessary, NTT Managers can keep track of L1 gas prices and change the gas limits accordingly.

**Wormhole Foundation:** This failure case can be handled by requesting redelivery with a higher gas limit. The current logic is the same as we use in our automatic relayers and we are ok with the current limitations of this design.

**Cyfrin:** Acknowledged.
