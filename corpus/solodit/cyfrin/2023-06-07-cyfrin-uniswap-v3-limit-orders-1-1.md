---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Withdrawing native assets may revert if wrapped native balance is zero
vuln_class: []
---

# Withdrawing native assets may revert if wrapped native balance is zero

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** The function `LimitOrderRegistry::withdrawNative` allows the owner to withdraw native and wrapped native assets from the contract. If balances of both are zero, calls to this function revert as there is nothing to withdraw.

```solidity
/**
 * @notice Allows owner to withdraw wrapped native and native assets from this contract.
 */
function withdrawNative() external onlyOwner {
    uint256 wrappedNativeBalance = WRAPPED_NATIVE.balanceOf(address(this));
    uint256 nativeBalance = address(this).balance;
    // Make sure there is something to withdraw.
    if (wrappedNativeBalance == 0 && nativeBalance == 0) revert LimitOrderRegistry__ZeroNativeBalance();
    WRAPPED_NATIVE.safeTransfer(owner, WRAPPED_NATIVE.balanceOf(address(this)));
    payable(owner).transfer(address(this).balance);
}
```

A zero value call with transfer non-zero wrapped native token balance will succeed just fine; however the call may revert in the opposite case. Given `safeTransfer` calls the wrapped native token's `transfer` function, the entire transaction for a non-zero value call with zero wrapped native token balance could revert if the wrapped native token reverts on zero-value transfers.

**Impact:** This would temporarily prevent the withdrawal of any native token balance until the wrapped native token balance is also non-zero, although it seems none of the wrapped native tokens revert on zero transfers on current intended target chains.

**Recommended Mitigation:** Separately validate the wrapped native token balance prior to attempting the transfer.

**GFX Labs:** Fixed by adding `if` statements to check the amount is non-zero before attempting to withdraw in commit [d2dd99c](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/d2dd99ccc30fd8534373be9ee0566603623e433d).

**Cyfrin:** Acknowledged. It is not necessary to revert - this line can be removed:
```solidity
if (wrappedNativeBalance == 0 && nativeBalance == 0) revert LimitOrderRegistry__ZeroNativeBalance();
```

**GFX Labs:** Acknowledged. Revert isn't strictly necessary, but also doesn't hurt.

**Cyfrin:** Acknowledged.
