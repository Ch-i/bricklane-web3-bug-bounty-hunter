---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Use named returns especially for `memory` outputs
vuln_class: []
---

# Use named returns especially for `memory` outputs

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** Use named returns especially for `memory` outputs, eg in `MTokenMessager::calculateCCSendTokenFeeAndMessage`:
```diff
    function calculateCCSendTokenFeeAndMessage(
        uint64 destinationChainSelector,
        address messageReceiver,
        address sender,
        address recipient,
        uint value,
        bytes calldata extraArgs
    )
        public
        view
        returns (uint256 fee, Client.EVM2AnyMessage memory evm2AnyMessage)
    {
        bytes memory data = ccipClient.msgOfCcSendToken(
            sender,
            recipient,
            value
        );
-       return
+       (fee, evm2AnyMessage) =
            getFeeAndMessage(
                destinationChainSelector,
                messageReceiver,
                extraArgs,
                data
            );
    }
```

Also applies to:
* `MTokenMessager::calculateCcSendMintBudgetFeeAndMessage`
* `MTokenMessager::sendDataToChain` where obsolete `return` can be removed
* the same functions in `MTokenMessagerV2`

**Matrixdock:** Fixed in commit [f3fbe97](https://github.com/Matrixdock-RWA/RWA-Contracts/commit/f3fbe97bd20ad514b76aa422a7dfc1f8a66cd66b#diff-f1dbc2c2c340ac285844595cba6f20040bb8b33c2ae726867955370039433c6aR82-R102) for `MTokenMessagerV2`.

**Cyfrin:** Verified.
