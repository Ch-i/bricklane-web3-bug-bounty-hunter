---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-10-17-carina-finance-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-10-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-10-17-Carina-Finance.md
tags:
- firm:codespect
- report:2025-10-17-carina-finance
title: '[M-01] Malicious solver can drain NativeTokenFlow contract via reentrancy'
vuln_class: []
---

# [M-01] Malicious solver can drain NativeTokenFlow contract via reentrancy

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-10-17-Carina-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-10-17-Carina-Finance.md)_

---

**Files:** [`NativeTokenFlow.sol`](https://github.com/carina-finance/carina-sc/blob/6ff2ad112b6b62acb054411b8181d9414970b08b/src/NativeTokenFlow.sol#L121)

**Description:**

The `NativeTokenFlow` contract allows users to create an order using the native token. Such an order is then fulfilled by a solver through the `Settlement` contract, after which the user receives the desired assets. A user can cancel their order via `cancelOrder(...)` before it is settled. If the order is successfully cancelled, the user is refunded the corresponding native token amount.

```solidity
if (orderFilledAmount < order.amountIn) {
    uint256 refundAmount = order.amountIn - orderFilledAmount;
    if (refundAmount > 0) {
        // ...

        (bool success,) = payable(orderMeta.owner).call{value: refundAmount}("");
        if (!success) {
            revert NativeTokenTransferFailed();
        }
    }
}
// ...
}
// ...
orderMeta.status = NATIVE_FLOW_ORDER_STATUS_CANCELLED;
```

However, as shown above, the cancellation status for the order is set after the low-level `call(...)`, which introduces a reentrancy vector. A malicious solver could exploit this vulnerability as follows:

1. Create their own order in the `NativeTokenFlow` contract;
2. Call `cancelOrder(...)` in the same contract;
3. When the refund is issued via `call(...)`, the attacker’s `receive(...)` function is triggered. From there, they can call `settle(...)` on the `Settlement` contract. This succeeds because `NativeTokenFlow::isValidSignature(...)` still considers the order valid (its status remains `NATIVE_FLOW_ORDER_STATUS_CREATED`).
4. As a result, the solver effectively uses the same `tokenIn` amount twice — first receiving a refund, and then fulfilling the order again.

**Impact:** Potential draining of the `NativeTokenFlow` contract. However, the overall impact is constrained by the actor’s ability to perform the attack and the available liquidity in the contract.

**Recommendation:** Set the cancellation status before performing the low-level call, e.g.:

```solidity
orderMeta.status = NATIVE_FLOW_ORDER_STATUS_CANCELLED;

// ...
(bool success,) = payable(orderMeta.owner).call{value: refundAmount}("");
```

**Status:** Fixed

**Client response:** Fixed in [3adbb8b541e3be631235179acfe1b3a416b2c230](https://github.com/carina-finance/carina-sc/pull/10/commits/3adbb8b541e3be631235179acfe1b3a416b2c230)
