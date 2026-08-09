---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: NatSpec documentation inconsistent with function/event signatures
vuln_class: []
---

# NatSpec documentation inconsistent with function/event signatures

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

Inline NatSpec documentation does not reflect the actual signatures in multiple cases:

1. Missing definition for the `recipientNttManagerAddress` in the `ITransceiver::sendMessage` [NatSpec](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/interfaces/ITransceiver.sol#L27-L32):
```solidity
/// @dev Send a message to another chain.
/// @param recipientChain The Wormhole chain ID of the recipient.
/// @param instruction An additional Instruction provided by the Transceiver to be
/// executed on the recipient chain.
/// @param nttManagerMessage A message to be sent to the nttManager on the recipient chain.
function sendMessage(
    uint16 recipientChain, //@note wormhole chain id
    TransceiverStructs.TransceiverInstruction memory instruction, //@note same as above
    bytes memory nttManagerMessage,
    bytes32 recipientNttManagerAddress
) external payable;
```

2. Missing definition for `sequence` in the `IRateLimiterEvents::OutboundTransferRateLimited` [NatSpec](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/interfaces/IRateLimiterEvents.sol#L19-L25):
```solidity
/// @notice Emitted when an outbound transfer is rate limited.
/// @dev Topic0
///      0x754d657d1363ee47d967b415652b739bfe96d5729ccf2f26625dcdbc147db68b.
/// @param sender The initial sender of the transfer.
/// @param amount The amount to be transferred.
/// @param currentCapacity The capacity left for transfers within the 24-hour window.
event OutboundTransferRateLimited(
    address indexed sender, uint64 sequence, uint256 amount, uint256 currentCapacity
);
```

**Wormhole Foundation:** Inline NatSpec docs can be error-prone. Thinking about using Foundry as the source of truth for selectors/topics.

**Cyfrin:** Acknowledged.
