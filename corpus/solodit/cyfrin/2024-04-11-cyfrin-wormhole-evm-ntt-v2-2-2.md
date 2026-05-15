---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-2
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
title: Incorrect Transceiver payload prefix definition
vuln_class: []
---

# Incorrect Transceiver payload prefix definition

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** The `WH_TRANSCEIVER_PAYLOAD_PREFIX` constant in `WormholeTransceiverState.sol` contains invalid ASCII bytes and, as such, does not match what is written in the inline developer documentation:
```solidity
/// @dev Prefix for all TransceiverMessage payloads
///      This is 0x99'E''W''H'
/// @notice Magic string (constant value set by messaging provider) that idenfies the payload as an transceiver-emitted payload.
///         Note that this is not a security critical field. It's meant to be used by messaging providers to identify which messages are Transceiver-related.
bytes4 constant WH_TRANSCEIVER_PAYLOAD_PREFIX = 0x9945FF10;
```
The correct payload prefix is `0x99455748`, which is output when running the following command:
```bash
cast --from-utf8 "EWH"
```

**Impact:** While still a valid 4-byte hex prefix, used purely for identification purposes, an incorrect prefix could cause downstream confusion and result in otherwise valid Transceiver payloads being incorrectly prefixed.

**Recommended Mitigation:** Update the constant definition to use the correct prefix corresponding to the documented string:
```diff
+ bytes4 constant WH_TRANSCEIVER_PAYLOAD_PREFIX = 0x99455748;
```

**Wormhole Foundation:** Changing this prefix has no material impact since it’s still a valid `bytes4` constant. We elected to keep this unchanged due to downstream dependencies.

**Cyfrin:** Acknowledged.
