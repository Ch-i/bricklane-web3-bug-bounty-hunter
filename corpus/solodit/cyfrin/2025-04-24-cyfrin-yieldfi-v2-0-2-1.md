---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Static `gasLimit` will result in overpayment
vuln_class: []
---

# Static `gasLimit` will result in overpayment

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** Since [unspent gas is not refunded](https://docs.chain.link/ccip/best-practices#setting-gaslimit), Chainlink recommends carefully setting the `gasLimit` within the `extraArgs` parameter to avoid overpaying for execution.

In [`BridgeCCIP::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L131), the `gasLimit` is hardcoded to `200_000`, which is also Chainlink’s default:

```solidity
extraArgs: Client._argsToBytes(Client.EVMExtraArgsV2({ gasLimit: 200_000, allowOutOfOrderExecution: true })),
```

This hardcoded value directly affects every user bridging tokens, as they will be consistently overpaying for execution costs on the destination chain.

**Recommended Mitigation:** A more efficient approach would be to measure the gas usage of the `_ccipReceive` function using tools like Hardhat or Foundry and set the `gasLimit` accordingly—adding a margin for safety. This ensures that the protocol avoids overpaying for gas on every cross-chain message.

This issue also reinforces the importance of making `extraArgs` mutable, so the gas limit and other parameters can be adjusted if execution costs change over time (e.g., due to protocol upgrades like [EIP-1884](https://eips.ethereum.org/EIPS/eip-1884)).

**YieldFi:** Fixed in commit [`3cc0b23`](https://github.com/YieldFiLabs/contracts/commit/3cc0b2331c35327a43e95176ce6c5578f145c0ee)

**Cyfrin:** Verified. `extraArgs` is now passed as a parameter to the call.
