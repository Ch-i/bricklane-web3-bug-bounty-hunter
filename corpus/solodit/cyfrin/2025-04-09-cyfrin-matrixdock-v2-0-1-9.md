---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Unnecessary code duplication in `MTokenMessager::sendDataToChain`
vuln_class: []
---

# Unnecessary code duplication in `MTokenMessager::sendDataToChain`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** The `sendDataToChain` function creates a message object and calculates fees, duplicating logic that already exists in the `getFeeAndMessage` function. This creates redundancy in the codebase, which can lead to inconsistencies during future updates and increases gas costs.

**Recommended Mitigation:** Refactor the `sendDataToChain` function to use the existing `getFeeAndMessage` function:

```diff
    function sendDataToChain(
        uint64 destinationChainSelector,
        address messageReceiver,
        bytes calldata extraArgs,
        bytes memory data
    ) internal returns (bytes32 messageId) {
-        Client.EVM2AnyMessage memory evm2AnyMessage = Client.EVM2AnyMessage({
-            receiver: abi.encode(messageReceiver),
-            data: data,
-            tokenAmounts: new Client.EVMTokenAmount[](0),
-            extraArgs: extraArgs,
-            feeToken: address(0)
-        });
-        uint256 fee = IRouterClient(getRouter()).getFee(
-            destinationChainSelector,
-            evm2AnyMessage
-        );
+        (uint256 fee, Client.EVM2AnyMessage memory evm2AnyMessage) = getFeeAndMessage(
+            destinationChainSelector,
+            messageReceiver,
+            extraArgs,
+            data
+        );
        if (msg.value < fee) {
            revert InsufficientFee(fee, msg.value);
        }
        messageId = IRouterClient(getRouter()).ccipSend{value: fee}(
            destinationChainSelector,
            evm2AnyMessage
        );
        if (msg.value - fee > 0) {
            payable(msg.sender).sendValue(msg.value - fee);
        }
        return messageId;
    }
```

The same issue is also present in `MTokenMessagerV2::sendDataToChain`.

**Matrixdock:** Fixed in commit [f3fbe97](https://github.com/Matrixdock-RWA/RWA-Contracts/commit/f3fbe97bd20ad514b76aa422a7dfc1f8a66cd66b#diff-f1dbc2c2c340ac285844595cba6f20040bb8b33c2ae726867955370039433c6aR183) for `MTokenMessagerV2`.

**Cyfrin:** Verified.



\clearpage
