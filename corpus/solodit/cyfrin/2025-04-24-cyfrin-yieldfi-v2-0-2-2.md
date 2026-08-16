---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Unverified `_receiver` can cause irrecoverable token loss
vuln_class: []
---

# Unverified `_receiver` can cause irrecoverable token loss

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** When a user bridges their YTokens using CCIP, they call [`BridgeCCIP::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L117-L158). One of the parameters passed to this function is `_receiver`, which is intended to be the destination contract on the receiving chain:

```solidity
function send(address _yToken, uint64 _dstChain, address _to, uint256 _amount, address _receiver) external payable notBlacklisted(msg.sender) notBlacklisted(_to) notPaused {
    require(_amount > 0, "!amount");
    require(lockboxes[_yToken] != address(0), "!token !lockbox");
    require(IERC20(_yToken).balanceOf(msg.sender) >= _amount, "!balance");
    require(_to != address(0), "!receiver");
    require(tokens[_yToken][_dstChain] != address(0), "!destination");

    bytes memory _encodedMessage = abi.encode(_dstChain, _to, tokens[_yToken][_dstChain], _amount, Constants.BRIDGE_SEND_HASH);

    // Sends the message to the destination endpoint
    Client.EVM2AnyMessage memory evm2AnyMessage = Client.EVM2AnyMessage({
        // @audit-issue `_receiver` not verified
        receiver: abi.encode(_receiver), // ABI-encoded receiver address
        data: abi.encode(_encodedMessage), // ABI-encoded string
        tokenAmounts: new Client.EVMTokenAmount[](0), // Empty array indicating no tokens are being sent
        extraArgs: Client._argsToBytes(Client.EVMExtraArgsV2({ gasLimit: 200_000, allowOutOfOrderExecution: true })),
        feeToken: address(0) // For msg.value
    });
```

However, the `_receiver` parameter is not validated. If the user provides an incorrect or malicious address, the message may be delivered to a contract that cannot handle it, resulting in unrecoverable loss of the bridged tokens.

**Recommended Mitigation:** Validate the `_receiver` address against a trusted mapping, such as the `peers` mapping mentioned in a previous finding, to ensure it corresponds to a legitimate contract on the destination chain.

**YieldFi:** Fixed in commit [`a03341d`](https://github.com/YieldFiLabs/contracts/commit/a03341d8103ba08473ea1cd39e64192608692aca)

**Cyfrin:** Verified. `_receiver ` is now verified to be a trusted peer.
