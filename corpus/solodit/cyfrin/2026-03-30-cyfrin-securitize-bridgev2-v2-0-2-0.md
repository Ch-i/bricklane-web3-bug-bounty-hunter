---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-30-cyfrin-securitize-bridgev2-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-bridgev2-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-30-cyfrin-securitize-bridgev2-v2-0
title: '`SecuritizeBridge::_bridgeDSTokensInternal` calls `publishMessage` before
  fee sufficiency check, wasting gas on revert'
vuln_class: []
---

# `SecuritizeBridge::_bridgeDSTokensInternal` calls `publishMessage` before fee sufficiency check, wasting gas on revert

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-30-cyfrin-securitize-bridgev2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-bridgev2-v2.0.md)_

---

**Description:** In `SecuritizeBridge::_bridgeDSTokensInternal`, `IWormhole::publishMessage` at L440 and `IExecutorQuoterRouter::quoteExecution` at L451 are both called before the fee sufficiency check at L460:

```solidity
// L440 - publishes message, costs significant gas
uint64 sequence = _wormholeCore.publishMessage{value: coreFee}(0, payload, consistencyLevel);

// L451-458 - quotes execution
uint256 execFee = _executorQuoterRouter.quoteExecution(...);

// L460 - fee check happens AFTER expensive operations
if (msg.value < coreFee + execFee) revert InsufficientETHForFees();
```

If the fee check reverts, EVM atomicity rolls back everything, so no funds are lost. However, significant gas is wasted executing `publishMessage` and `quoteExecution` before determining that the user sent insufficient ETH.

The contract already has `SecuritizeBridge::_quoteBridge` (L584-602) which demonstrates how to pre-compute fees using `IWormhole::nextSequence` instead of the actual published sequence, making it feasible to check fees first.

**Recommended Mitigation:** Move the fee check before `publishMessage` by using `nextSequence` to pre-compute the quote:

```solidity
uint256 coreFee = _wormholeCore.messageFee();
uint64 sequence = _wormholeCore.nextSequence(address(this));
bytes memory request = ExecutorMessages.makeVAAv1Request(_whChainId, _addressToBytes32(address(this)), sequence);
bytes memory relayInstructions = RelayInstructions.encodeGas(gasLimit, msgValue);
uint256 execFee = _executorQuoterRouter.quoteExecution(
    _targetChain, targetBridgeAddress, _msgSender(), _quoterAddr, request, relayInstructions
);
if (msg.value < coreFee + execFee) revert InsufficientETHForFees();

// Now proceed with publishMessage and burn
```

**Securitize:** Acknowledged.

\clearpage
