---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Disabled Transceivers cannot be re-enabled by calling `TransceiverRegistry::_setTransceiver`
  after 64 have been registered
vuln_class: []
---

# Disabled Transceivers cannot be re-enabled by calling `TransceiverRegistry::_setTransceiver` after 64 have been registered

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** [`TransceiverRegistry::_setTransceiver`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/TransceiverRegistry.sol#L112-L153) handles the registering of Transceivers, but note that they cannot be re-registered as this has other downstream effects, so this function is also responsible for the re-enabling of previously registered but currently disabled Transceivers.
```solidity
function _setTransceiver(address transceiver) internal returns (uint8 index) {
    /* snip */
    if (transceiver == address(0)) {
        revert InvalidTransceiverZeroAddress();
    }

    if (_numTransceivers.registered >= MAX_TRANSCEIVERS) {
        revert TooManyTransceivers();
    }

    if (transceiverInfos[transceiver].registered) {
        transceiverInfos[transceiver].enabled = true;
    } else {
    /* snip */
}
```

This function reverts if the passed transceiver address is `address(0)` or the number of registered transceivers is already at its defined maximum of 64. Assuming a total of 64 registered Transceivers, with some of these Transceivers having been previously disabled, the placement of this latter validation will prevent a disabled Transceiver from being re-enabled since the subsequent block in which the storage indicating its enabled state is set to `true` is not reachable. Consequently, it will not be possible to re-enable any disabled transceivers after having registered the maximum number of Transceivers, meaning that this function will never be callable without redeployment.

**Impact:** Under normal circumstances, this maximum number of registered Transceivers should never be reached, especially since the underlying Transceivers are upgradeable. However, while unlikely based on operational assumptions, this undefined behavior could have a high impact, and so this is classified as a **MEDIUM** severity finding.

**Recommended Mitigation:** Move the placement of the maximum Transceivers validation to within the `else` block that is responsible for handling the registration of new Transceivers.

**Wormhole Foundation:** Fixed in [PR \#253](https://github.com/wormhole-foundation/example-native-token-transfers/pull/253).

**Cyfrin:** Verified. The validation is now skipped for previously registered (but currently disabled) Transceivers.
