---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-4-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Order read twice in `Manager::executeOrder`
vuln_class: []
---

# Order read twice in `Manager::executeOrder`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In [`Manager::executeOrder`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L207-L214) the order data is fetched from the Receipt:
```solidity
Order memory order = IReceipt(receipt).readOrder(_receiptId);
require(block.timestamp > order.eligibleAt, "!waitingPeriod");
require(_fee <= Constants.ONE_PERCENT, "!fee");
if (order.orderType) {
    _deposit(msg.sender, _receiptId, _amount, _fee, _gas);
} else {
    _withdraw(msg.sender, _receiptId, _amount, _fee, _gas);
}
```
Then order is read again in both [`Manager::_deposit`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L252-L253):
```solidity
function _deposit(address _caller, uint256 _receiptId, uint256 _shares, uint256 _fee, uint256 _gasFeeShares) internal {
    Order memory order = IReceipt(receipt).readOrder(_receiptId);
```

and [`Manager::_withdraw`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L327-L328):
```solidity
function _withdraw(address _caller, uint256 _receiptId, uint256 _assetAmountOut, uint256 _fee, uint256 _gasFeeShares) internal {
    Order memory order = IReceipt(receipt).readOrder(_receiptId);
```

This extra read is unnecessary. Consider passing the `Order memory order` as a parameter to `Manager::_deposit` and `Manager::_withdraw` instead. Thus saving to read the data again from the receipt:
```solidity
function _deposit(..., Order memory order) internal {

function _withdraw(..., Order memory order) internal {
```

**YieldFi:** Fixed in commit [`823b010`](https://github.com/YieldFiLabs/contracts/commit/823b010d74fd55fb88b31619c1a94dac2ef65ad3)

**Cyfrin:** Verified.

\clearpage
