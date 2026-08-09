---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Hardcoded `extraArgs` violates CCIP best practices
vuln_class: []
---

# Hardcoded `extraArgs` violates CCIP best practices

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** When sending cross-chain messages via CCIP, Chainlink recommends keeping the `extraArgs` parameter mutable to allow for future upgrades or configuration changes, as outlined in their [best practices](https://docs.chain.link/ccip/best-practices#using-extraargs).

However, this recommendation is not followed in [`BridgeCCIP::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L126-L133), where `extraArgs` is hardcoded:
```solidity
// Sends the message to the destination endpoint
Client.EVM2AnyMessage memory evm2AnyMessage = Client.EVM2AnyMessage({
    receiver: abi.encode(_receiver), // ABI-encoded receiver address
    data: abi.encode(_encodedMessage), // ABI-encoded string
    tokenAmounts: new Client.EVMTokenAmount[](0), // Empty array indicating no tokens are being sent
    // @audit-issue `extraArgs` hardcoded
    extraArgs: Client._argsToBytes(Client.EVMExtraArgsV2({ gasLimit: 200_000, allowOutOfOrderExecution: true })),
    feeToken: address(0) // For msg.value
});
```

**Impact:** Because `extraArgs` is hardcoded, any future changes would require deploying a new version of the bridge contract.

**Recommended Mitigation:** Consider making `extraArgs` mutable by either passing it as a parameter to the `send` function or deriving it from configurable contract storage.

**YieldFi:** Fixed in commits [`3cc0b23`](https://github.com/YieldFiLabs/contracts/commit/3cc0b2331c35327a43e95176ce6c5578f145c0ee) and [`fd4b7ab5`](https://github.com/YieldFiLabs/contracts/commit/fd4b7ab57a5ae2ac366b4d9d086eb372defc7f8c)

**Cyfrin:** Verified. `extraArgs` is now passed as a parameter to the call.
