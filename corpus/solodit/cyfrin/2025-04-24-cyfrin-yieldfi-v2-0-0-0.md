---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Missing source validation in CCIP message handling
vuln_class: []
---

# Missing source validation in CCIP message handling

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** YieldFi integrates with Chainlink CCIP to facilitate cross-chain transfers of its yield tokens (`YToken`). This functionality is handled by the `BridgeCCIP` contract, which manages token accounting for these transfers.

However, in the [`BridgeCCIP::_ccipReceive`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L160-L181) function, there is no validation of the message sender from the source chain:
```solidity
/// handle a received message
function _ccipReceive(Client.Any2EVMMessage memory any2EvmMessage) internal override {
    bytes memory message = abi.decode(any2EvmMessage.data, (bytes)); // abi-decoding of the sent text
    BridgeSendPayload memory payload = Codec.decodeBridgeSendPayload(message);
    bytes32 _hash = keccak256(abi.encode(message, any2EvmMessage.messageId));
    require(!processedMessages[_hash], "processed");

    processedMessages[_hash] = true;

    require(payload.amount > 0, "!amount");

    ...
}
```

As a result, an attacker could craft a malicious `Any2EVMMessage` containing valid data and trigger the minting or unlocking of arbitrary tokens by sending it through CCIP to the `BridgeCCIP` contract.


**Impact:** An attacker could drain the bridge of tokens on L1 or mint an unlimited amount of tokens on L2. While a two-step redeem process offers some mitigation, such an exploit would still severely disrupt the protocol’s accounting and could be abused when claiming yield for example.

**Recommended Mitigation:** Consider implementing validation to ensure that messages are only accepted from trusted peers on the source chain:
```solidity
mapping(uint64 sourceChain => mapping(address peer => bool allowed)) public allowedPeers;
...
function _ccipReceive(
    Client.Any2EVMMessage memory any2EvmMessage
) internal override {
    address sender = abi.decode(any2EvmMessage.sender, (address));
    require(allowedPeers[any2EvmMessage.sourceChainSelector][sender],"allowed");
    ...
```

**YieldFi:** Fixed in commit [`a03341d`](https://github.com/YieldFiLabs/contracts/commit/a03341d8103ba08473ea1cd39e64192608692aca)

**Cyfrin:** Verified. `sender` is now verified to be a trusted sender.
