---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Hardcoded CCIP `feeToken` prevents LINK discount usage
vuln_class: []
---

# Hardcoded CCIP `feeToken` prevents LINK discount usage

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In `BridgeCCIP::send`, the [`feeToken`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L126-L133) parameter is hardcoded:
```solidity
// Sends the message to the destination endpoint
Client.EVM2AnyMessage memory evm2AnyMessage = Client.EVM2AnyMessage({
    receiver: abi.encode(_receiver), // ABI-encoded receiver address
    data: abi.encode(_encodedMessage), // ABI-encoded string
    tokenAmounts: new Client.EVMTokenAmount[](0), // Empty array indicating no tokens are being sent
    extraArgs: Client._argsToBytes(Client.EVMExtraArgsV2({ gasLimit: 200_000, allowOutOfOrderExecution: true })),
    // @audit-issue hardcoded fee token
    feeToken: address(0) // For msg.value
});
```

Chainlink CCIP supports paying fees using either the native gas token or `LINK`. By hardcoding `feeToken = address(0)`, the protocol forces all users to pay with the native gas token, removing flexibility.

This design choice simplifies implementation but has cost implications: CCIP offers a [10% fee discount](https://docs.chain.link/ccip/billing#network-fee-table) when using `LINK`, so users holding `LINK` are unable to take advantage of these reduced fees.

**Recommended Mitigation:** Consider allowing users to choose their preferred payment token—either `LINK` or native gas—based on their individual cost and convenience preferences.

**YieldFi:** Fixed in commits [`3cc0b23`](https://github.com/YieldFiLabs/contracts/commit/3cc0b2331c35327a43e95176ce6c5578f145c0ee) and [`e9c160f`](https://github.com/YieldFiLabs/contracts/commit/e9c160fdfd6dd90650c9537fba73c17cb3c53ea5)

**Cyfrin:** Verified.
