---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Asymmetry in Transceiver pausing capability
vuln_class: []
---

# Asymmetry in Transceiver pausing capability

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** Pausing functionality is exposed via `Transceiver::_pauseTransceiver`; however, there is no corresponding function that exposes unpausing functionality:
```solidity
/// @dev pause the transceiver.
function _pauseTransceiver() internal {
    _pause();
}
```

**Impact:** While not an immediate issue since the above function is not currently in use anywhere, this should be resolved to avoid cases where Transceivers could become permanently paused.

**Recommended Mitigation:**
```diff
+ /// @dev unpause the transceiver.
+ function _unpauseTransceiver() internal {
+     _unpause();
+ }
```

**Wormhole Foundation:** Fixed in [PR \#273](https://github.com/wormhole-foundation/example-native-token-transfers/pull/273).

**Cyfrin:** Verified. `Transceiver::_pauseTransceiver` has been removed.
