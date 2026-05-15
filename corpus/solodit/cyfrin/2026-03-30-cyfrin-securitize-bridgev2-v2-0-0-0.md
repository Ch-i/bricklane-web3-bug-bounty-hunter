---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-30-cyfrin-securitize-bridgev2-v2-0-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-30T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-bridgev2-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-30-cyfrin-securitize-bridgev2-v2-0
title: '`USDCBridgeV2::_quoteBridge` hardcodes `msgValue=0` creating fee mismatch
  that bricks the USDC bridge when gas dropoff is configured'
vuln_class: []
---

# `USDCBridgeV2::_quoteBridge` hardcodes `msgValue=0` creating fee mismatch that bricks the USDC bridge when gas dropoff is configured

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-30-cyfrin-securitize-bridgev2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-bridgev2-v2.0.md)_

---

**Description:** `USDCBridgeV2::_quoteBridge` computes the executor fee using `RelayInstructions.encodeGas(gasLimit, 0)` with a hardcoded zero for the gas dropoff parameter:

```solidity
function _quoteBridge(uint16 _targetChain) private view returns (uint256 execFee) {
    bytes memory request = ExecutorMessages.makeCCTPv2Request();
@>  bytes memory relayInstructions = RelayInstructions.encodeGas(gasLimit, 0); // hardcoded 0
    execFee = executorQuoterRouter.quoteExecution(
        _targetChain, bytes32(0), address(this), quoterAddr, request, relayInstructions
    );
}
```

However, `USDCBridgeV2::sendUSDCCrossChainDeposit` calls `requestExecution` with the actual stored `msgValue`:

```solidity
executorQuoterRouter.requestExecution{value: execFee}(
    _targetChain,
    bytes32(0),
    address(this),
    quoterAddr,
    ExecutorMessages.makeCCTPv2Request(),
@>  RelayInstructions.encodeGas(gasLimit, msgValue) // actual msgValue
);
```

When admin sets `msgValue > 0` via `USDCBridgeV2::updateMsgValue`, the fee quoted by `_quoteBridge` is lower than what the executor actually requires for the relay instructions passed to `requestExecution`. The balance check at L215 (`address(this).balance < execFee`) uses this underestimated fee, allowing the transaction to proceed with insufficient ETH for the actual execution cost.

**Impact:** When admin configures `msgValue > 0` via `USDCBridgeV2::updateMsgValue`, the USDC bridge is completely bricked — every `USDCBridgeV2::sendUSDCCrossChainDeposit` call reverts and no USDC can be bridged until admin resets `msgValue` to 0.

The Wormhole `ExecutorQuoterRouter::requestExecution` ([source](https://github.com/wormholelabs-xyz/example-messaging-executor/blob/main/evm/src/ExecutorQuoterRouter.sol)) re-computes the required fee from the **actual relay instructions passed in the same call** (not from a prior quote). It parses the `relayInstructions` bytes to extract `gasLimit` and `msgValue`, converts them to source chain value, and checks `msg.value >= requiredPayment`. If insufficient, it reverts with `Underpaid(provided, expected)`.

Since the revert occurs within the same atomic transaction, the preceding USDC `safeTransferFrom` and CCTP `depositForBurn` are also rolled back — no USDC is permanently lost. However, the bridge is non-functional for its intended purpose: bridging USDC with gas dropoff configured.

**Recommended Mitigation:** Use `msgValue` in `_quoteBridge` to match the relay instructions actually passed to `requestExecution`:

```diff
function _quoteBridge(uint16 _targetChain) private view returns (uint256 execFee) {
    bytes memory request = ExecutorMessages.makeCCTPv2Request();
-   bytes memory relayInstructions = RelayInstructions.encodeGas(gasLimit, 0);
+   bytes memory relayInstructions = RelayInstructions.encodeGas(gasLimit, msgValue);
    execFee = executorQuoterRouter.quoteExecution(
        _targetChain, bytes32(0), address(this), quoterAddr, request, relayInstructions
    );
}
```

**Securitize:** Fixed in commit [c313304](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/c31330414ae1c0d7dd9477fd6e02411ce56fd1a0)

**Cyfrin:** Verified. Call to `RelayInstructions::encodeGas` is now called with `msgValue` instead of hardcoding the value to`0`
