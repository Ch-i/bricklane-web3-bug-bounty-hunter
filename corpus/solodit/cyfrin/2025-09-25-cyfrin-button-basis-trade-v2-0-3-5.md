---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Consider enabling on-behalf-of withdrawals
vuln_class: []
---

# Consider enabling on-behalf-of withdrawals

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** `BasisTradeVault`’s withdrawal queue only supports self-initiated requests that always pay the requester (`receiver = msg.sender`). For better ERC-4626 alignment and composability (routers, managers, third party integrations), extend the existing queue API to accept an explicit `receiver` and persist caller / owner / receiver in the queue item. Then use these values when processing to transfer assets to `receiver` and emit the canonical ERC-4626 `Withdraw(caller, receiver, owner, assets, shares)` event correctly.

Consider extending the queued item to persist new addresses:
```solidity
struct WithdrawalRequest {
    address owner;     // share owner whose shares were escrowed
    address receiver;  // recipient of assets on payout
    address caller;    // who enqueued the request
    uint256 shares;
    uint256 assets;
    uint256 timestamp;
}
```
Update existing event:
```solidity
struct WithdrawalRequested {
    address owner;
    address receiver;
    address caller;
    uint256 shares;
    uint256 assets;
    uint256 timestamp;
}
```
and change the request function signatures together with consuming the allowance:
```
function requestWithdraw(
    uint256 assets,
    address receiver,
    address owner
) external returns (uint256 queuePosition) {
    require(assets > 0, "Cannot withdraw 0 assets");
    uint256 grossAssets = assets + _calculateFeeAmount(assets, withdrawalFeeBps);
    uint256 shares = _convertToShares(grossAssets, Math.Rounding.Ceil);
    return requestRedeem(shares, receiver, owner);
}

function requestRedeem(
    uint256 shares,
    address receiver,
    address owner
) public requirePocket returns (uint256 queuePosition) {
    address caller = msg.sender;

    require(receiver != address(0), "Invalid receiver");
    require(owner != address(0), "Invalid owner");
    require(shares > 0, "Cannot redeem 0 shares");

    // spend allowance when acting on behalf of `owner`
    if (caller != owner) {
        _spendAllowance(owner, caller, shares);
    }

    // ...

    emit WithdrawalRequested(caller, owner, receiver, assetsAfterFee, shares, fee, queuePosition);
}
```
And lastly use stored identities in processing
```solidity
function processWithdrawal() external onlyAgent {
    require(queueHead < queueTail, "No withdrawals to process");

    uint256 currentQueuePosition = queueHead;
    WithdrawalRequest memory request = withdrawalQueue[currentQueuePosition];
    require(request.owner != address(0), "Invalid withdrawal request");

    // Ensure sufficient vault liquidity
    uint256 vaultBalance = IERC20(asset()).balanceOf(address(this));
    require(vaultBalance >= request.assets, "Insufficient vault balance for withdrawal");

    // Burn escrowed shares and advance queue
    _burn(address(this), request.shares);
    totalEscrowedShares -= request.shares;
    totalPendingWithdrawals -= request.assets;
    delete withdrawalQueue[currentQueuePosition];
    queueHead++;

    // Pay the correct receiver
    IERC20(asset()).safeTransfer(request.receiver, request.assets);

    // Emit canonical ERC-4626 Withdraw with correct identities
    emit Withdraw(request.caller, request.receiver, request.owner, request.assets, request.shares);
    emit WithdrawalProcessed(request.owner, request.assets, currentQueuePosition);
}
```

This change maintains current safety (shares are escrowed immediately), improves interoperability, and ensures events and payouts reflect the actual caller/owner/receiver roles.


**Button:** Implemented in commit [`9cde24c`](https://github.com/buttonxyz/button-protocol/commit/9cde24caa4b3f5f37a059bb2fde172cfa374d3a9)

**Cyfrin:** Verified. Caller/owner/receiver now stored and used in the event as well as approvals used in `requestRedeem`.
