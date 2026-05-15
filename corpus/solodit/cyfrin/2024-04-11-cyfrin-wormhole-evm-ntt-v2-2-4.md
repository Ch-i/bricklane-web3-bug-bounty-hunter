---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Missing threshold invariant check when adding/removing transceivers
vuln_class: []
---

# Missing threshold invariant check when adding/removing transceivers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** [`NttManagerState::_checkThresholdInvariants`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/NttManagerState.sol#L371-L385) is intended to check invariant properties related to the threshold storage and is called on initialization, migration, and access-controlled setting of the threshold storage directly. However, this function is not currently called when the [`setTransceiver()`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/NttManagerState.sol#L205-L228) and [removeTransceiver()](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/NttManagerState.sol#L230-L242) functions execute, which also access and modify the relevant state.

**Impact:** A bug in the addition/removal of transceivers could go unnoticed since the inline invariant checks on the threshold storage are not being performed here despite being modified.

**Recommended Mitigation:** Ensure `NttManagerState::_checkThresholdInvariants` is called within `NttManagerState::setTransceiver` and `NttManagerState::removeTransceiver`.

**Wormhole Foundation:** Fixed in [PR \#381](https://github.com/wormhole-foundation/example-native-token-transfers/pull/381).

**Cyfrin:** Verified. The threshold invariants are now checked when Transceivers are both added and removed. As noted, this change prevents an admin from disabling all the transceivers from an NTT manager, meaning there has to be at least 1 enabled Transceiver at all times when `numRegisteredTransceivers > 0`.

\clearpage
