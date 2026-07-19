---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-4-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Optimize invariant check iterations in `TransceiverRegistry::_checkTransceiversInvariants`
vuln_class: []
---

# Optimize invariant check iterations in `TransceiverRegistry::_checkTransceiversInvariants`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

The first loop over all enabled transceivers in [`TransceiverRegistry::_checkTransceiversInvariants`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/TransceiverRegistry.sol#L211-L234) could instead be included in the top level of the nested loop directly below to save multiple iterations and hence gas.
```diff
function _checkTransceiversInvariants() internal view {
    _NumTransceivers storage _numTransceivers = _getNumTransceiversStorage();
    address[] storage _enabledTransceivers = _getEnabledTransceiversStorage();

    uint256 numTransceiversEnabled = _numTransceivers.enabled;
    assert(numTransceiversEnabled == _enabledTransceivers.length);

-   for (uint256 i = 0; i < numTransceiversEnabled; i++) {
-       _checkTransceiverInvariants(_enabledTransceivers[i]);
-   }
-
    // invariant: each transceiver is only enabled once
    for (uint256 i = 0; i < numTransceiversEnabled; i++) {
+       _checkTransceiverInvariants(_enabledTransceivers[i]);
        for (uint256 j = i + 1; j < numTransceiversEnabled; j++) {
            assert(_enabledTransceivers[i] != _enabledTransceivers[j]);
        }
    }

    // invariant: numRegisteredTransceivers <= MAX_TRANSCEIVERS
    assert(_numTransceivers.registered <= MAX_TRANSCEIVERS);
}
```

**Wormhole Foundation:** Admin only method so gas usage is not as critical.

**Cyfrin:** Acknowledged.

\clearpage
