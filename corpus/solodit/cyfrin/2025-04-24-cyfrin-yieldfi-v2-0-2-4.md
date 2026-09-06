---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Chainlink router configured twice
vuln_class: []
---

# Chainlink router configured twice

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In `BridgeCCIP`, there is a dedicated storage slot for the CCIP router address, [`router`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L32-L33):

```solidity
contract BridgeCCIP is CCIPReceiver, Ownable {
    address public router;
```

This value can be updated by the admin through [`BridgeCCIP::setRouter`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L69-L73):

```solidity
function setRouter(address _router) external onlyAdmin {
    require(_router != address(0), "!router");
    router = _router;
    emit SetRouter(msg.sender, _router);
}
```

The `router` is then used in [`BridgeCCIP::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L157) to send messages via CCIP:

```solidity
IRouterClient(router).ccipSend{ value: msg.value }(_dstChain, evm2AnyMessage);
```

However, the inherited `CCIPReceiver` contract already defines an immutable router address (`i_ccipRouter`), which is used to validate that incoming CCIP messages originate from the correct router.

This introduces an inconsistency: if `BridgeCCIP.router` is changed, the contract will continue to *send* messages via the new router, but *receive* messages only from the original, immutable `i_ccipRouter`. This mismatch could break cross-chain communication or make message delivery non-functional.

**Recommended Mitigation:** Since the router address in `CCIPReceiver` is immutable, any future change to the router would already require redeployment of the `BridgeCCIP` contract. Therefore, the `router` storage slot and the `setRouter` function in `BridgeCCIP` are redundant and potentially misleading. We recommend removing both and relying exclusively on the `i_ccipRouter` value inherited from `CCIPReceiver`.

**YieldFi:** Fixed in commit [`3cc0b23`](https://github.com/YieldFiLabs/contracts/commit/3cc0b2331c35327a43e95176ce6c5578f145c0ee)

**Cyfrin:** Verified. `router` removed and `i_ccipRouter` used from the inherited contract.
