---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: '`AccountableAsyncRedeemVault::fulfillCancelRedeemRequest` can de-sync request
  data causing permanent DOS for queue processing'
vuln_class: []
---

# `AccountableAsyncRedeemVault::fulfillCancelRedeemRequest` can de-sync request data causing permanent DOS for queue processing

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** `fulfillCancelRedeemRequest()` function first finalises the cancellation of the redeeem request with input `requestID`, and then calls `_reduce()` to update the request state and `totalQueuedShares`.

```solidity
    function fulfillCancelRedeemRequest(address controller) public onlyOperatorOrStrategy {
        _fulfillCancelRedeemRequest(_requestIds[controller], controller);
        _reduce(controller, _vaultStates[controller].pendingRedeemRequest);
    }
```

The problem here is that it is using current value of `_vaultStates[controller].pendingRedeemRequest` in the `_reduce()` call, but it has been set to zero in `_fulfillCancelRedeemRequest()`.

This means `_reduce()` here will always be called with zero shares, and it does not revert when shares input is zero. But it corrupts the request struct and `totalQueuedShares` value.

The request will still exist with actual shares values, and create problems in usual batch processing of the queue.

One example of the resulting impact is this :
1. User X places a redeem request for 100 shares
2. User X cancels this redeem request
3. His request is not fulfilled instantly (this depends on the strategy)
4. Operator calls `fulfillCancelRedeemRequest()` to process this cancellation.
5. The call goes through properly. As a result [state.pendingRedeemRequest = 0] but the request state still has request.shares == 100 and other values. Also, the `_queue.nextRequestID` remains unchanged.
6. Now when batch processing proceeds via `processUpToShares()`, it is guaranteed that User X's requestID will also be processed (it is still in the queue from nextRequestID to lastRequestID) and when that happens, it will suffer a revert in `_processUptoShares()` => `_fulfillRedeemRequest()` because `state.pendingRedeemRequest` was set to == 0 in step 5.

```solidity
    function _fulfillRedeemRequest(uint128 requestId, address controller, uint256 shares, uint256 price)
        internal
        override
    {
        VaultState storage state = _vaultStates[controller];
        if (state.pendingRedeemRequest == 0) revert NoRedeemRequest();
        if (state.pendingRedeemRequest < shares) revert InsufficientAmount();
        if (state.pendingCancelRedeemRequest) revert RedeemRequestWasCancelled();
```


**Impact:** If this function is ever called, there will be a permanent de-sync between the values stored as per requestID data and the vaultState of the controller, which will interfere with queue processing in different ways.

The example showcased here is a critical DOS blocking queue processing permanently. This will happen for strategies that offer async cancellation processing, but since vault is expected to be compatible with this behavior, fixing this is critical.


**Recommended Mitigation:**
```solidity
    function fulfillCancelRedeemRequest(address controller) public onlyOperatorOrStrategy {

+++        uint256 pendingShares = state.pendingRedeemRequest;
               _fulfillCancelRedeemRequest(_requestIds[controller], controller);
---          _reduce(controller, _vaultStates[controller].pendingRedeemRequest);
+++        _reduce(controller, pendingShares);
    }
```

**Accountable:** Fixed in commit [`84946dd`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/84946dd49dd70f9f5dfe40184beb52b734362701)

**Cyfrin:** Verified. `pendingShares` now cached before fulfill and then passed as argument to `_reduce`.
