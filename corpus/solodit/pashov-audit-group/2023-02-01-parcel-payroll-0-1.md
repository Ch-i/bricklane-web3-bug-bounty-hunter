---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[C-02] Contract fails to handle `address(0)` as a native asset for it''s zero
  balance left invariant'
vuln_class: []
---

# [C-02] Contract fails to handle `address(0)` as a native asset for it's zero balance left invariant

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

**Impact:**
High, as all transactions that use native assets will revert

**Likelihood:**
High, as it is well expected that native assets will be used as a `paymentToken` often

**Description**

The `executePayroll` method has the following code at the end of it:

```solidity
// Check if the contract has any tokens left
for (uint256 i = 0; i < paymentTokens.length; i++) {
    IERC20 erc20 = IERC20(paymentTokens[i]);
    if (erc20.balanceOf(address(this)) > 0) {
        // Revert if the contract has any tokens left
        revert("CS018");
    }
}
```

A few lines above the code looks like this:

```solidity
if (tokenAddress[i] == address(0)) {
    // Transfer ether
    payable(to[i]).transfer(amount[i]);
    packPayoutNonce(true, payoutNonce[i]);
}
```

Which shows us that `address(0)` is used to handle native assets transfers. The problem is that the formerly mentioned code does not handle this `address(0)` token correctly, so if the `paymentTokens` array contains it the whole transaction will revert.

**Recommendations**

Check separately for the native asset balance of the contract in the end of `executePayroll` and ignore `address(0)` when calling `ERC20::balanceOf` for the `paymentTokens` array values.
