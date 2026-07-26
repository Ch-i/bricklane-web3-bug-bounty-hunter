---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Potential risk if callback logic is enabled in the future
vuln_class: []
---

# Potential risk if callback logic is enabled in the future

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** Both the `Manager` and `PerpetualBond` contracts implement a two-step process for user interactions. As part of these calls, users can provide a `_callback` address and accompanying `_callbackData`. For example, here are the parameters for [`Manager::deposit`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L144):

```solidity
function deposit(..., address _callback, bytes calldata _callbackData) external notPaused nonReentrant {
```

However, these parameters are currently not passed along when the request is stored, as shown later in [`Manager::deposit`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L153):

```solidity
uint256 receiptId = IReceipt(receipt).mint(msg.sender, Order(..., address(0), ""));
```

Here, `address(0)` and empty `""` are hardcoded instead of using the user-supplied values.

Later, in the `executeOrder` flow (e.g., [`Manager::executeOrder`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L219-L223)), the callback is conditionally executed:

```solidity
// Execute the callback
if (order.callback != address(0)) {
    (bool success, ) = order.callback.call(order.callbackData);
    require(success, "callback failed");
}
```

If the original user-provided `_callback` and `_callbackData` were passed through and used here, it would pose a serious security risk. Malicious users could exploit this to execute arbitrary external calls and potentially steal tokens that are approved to the `Manager` or `PerpetualBond` contracts.

If callback functionality is not currently intended, consider removing or disabling the `_callback` and `_callbackData` parameters entirely to avoid the risk of these being enabled in the future. Alternatively, ensure strict validation and access control if support for callbacks is added later.


**YieldFi:** Acknowledged.
