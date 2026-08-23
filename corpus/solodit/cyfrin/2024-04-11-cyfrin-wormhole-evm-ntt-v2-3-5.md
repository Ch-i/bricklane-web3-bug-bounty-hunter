---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Canonical NTT chain ID should be fetched directly from Wormhole or mapped accordingly
vuln_class: []
---

# Canonical NTT chain ID should be fetched directly from Wormhole or mapped accordingly

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

Currently, the immutable `chainId` variable is assigned the value passed to the `NttManager` [constructor](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/NttManager.sol#L26-L32
) by the deployer:

```solidity
constructor(
    address _token,
    Mode _mode,
    uint16 _chainId,
    uint64 _rateLimitDuration
) NttManagerState(_token, _mode, _chainId, _rateLimitDuration) {}
```

However, no validation is performed to ensure that the chain identifier provided is as expected. Since this is intended to be the Wormhole chain ID, it should be validated against the value returned by the Wormhole contract. Otherwise, if the chain identifier does not match the Wormhole chain identifier, given the understanding that the ID is not necessarily required to be the Wormhole chain ID, then this state should be included within the `WormholeTransceiver` payload [published](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/Transceiver/WormholeTransceiver/WormholeTransceiverState.sol#L80) to Wormhole since it will differ from the emitter chain included in the VAA.

If it is decided to make the Wormhole chain ID the canonical chain ID, different Transceiver implementations should map to the corresponding chain ID representations within their logic. As such, the Wormhole address should be passed to the constructor of the NTT Manager, querying the chain ID directly from the Wormhole Core Bridge instead of taking an arbitrary value in the constructor as described above.

**Wormhole Foundation:** We have elected not to fetch the chain id directly from the core bridge in order to make this less opinionated. This will be documented and the mapping of chain ids can be implemented when required.

**Cyfrin:** Acknowledged.

\clearpage
