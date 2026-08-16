---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: '`WormholeTransceiver` EVM chain IDs storage cannot be updated'
vuln_class: []
---

# `WormholeTransceiver` EVM chain IDs storage cannot be updated

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

In the unlikely but possible scenario in which a registered EVM-compatible chain diverges as the result of an upgrade, the existing implementation of [`WormholeTransceiverState::setIsWormholeEvmChain`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/Transceiver/WormholeTransceiver/WormholeTransceiverState.sol#L228-L236) means that it will not be possible to update the corresponding storage. If, for whatever reason, a chain such as Optimism decides to move away from EVM (the opposite of what happened in reality, going from OVM to EVM), its chain ID will now correspond to a non-EVM chain. As such, this function should take a boolean argument, similar to the [other functions](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/Transceiver/WormholeTransceiver/WormholeTransceiverState.sol#L238-L256) defined below this one:
```diff
- function setIsWormholeEvmChain(uint16 chainId) external onlyOwner {
+ function setIsWormholeEvmChain(uint16 chainId, bool isEvm) external onlyOwner {
    if (chainId == 0) {
        revert InvalidWormholeChainIdZero();
    }
-     _getWormholeEvmChainIdsStorage()[chainId] = TRUE;
+     _getWormholeEvmChainIdsStorage()[chainId] = toWord(isEvm);

-     emit SetIsWormholeEvmChain(chainId);
+     emit SetIsWormholeEvmChain(chainId, isEvm);
}
```
The `SetIsWormholeEvmChain` event will also need to be modified to take this additional boolean field.

**Wormhole Foundation:** Fixed in [PR \#252](https://github.com/wormhole-foundation/example-native-token-transfers/pull/252).

**Cyfrin:** Verified. The storage can now be modified due to the addition of an `isEvm` boolean argument.
