---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-3-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: Insufficient delegate address validation in `NativeTokenPaymentEnforcer`
vuln_class: []
---

# Insufficient delegate address validation in `NativeTokenPaymentEnforcer`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** The `NativeTokenPaymentEnforcer` contract's `afterAllHook()` function calls `delegationManager.redeemDelegations()` to process a payment using an allowance delegation. However, it doesn't properly validate that the delegate address in the allowance delegation is either the enforcer contract itself (`address(this)`) or the special `ANY_DELEGATE` address.

```solidity
   // NativeTokenPaymentEnforcer.sol
    function afterAllHook( ... ) ... {
        ...
        Delegation[] memory allowanceDelegations_ = abi.decode(_args, (Delegation[]));

        ...
        // Attempt to redeem the delegation and make the payment
>>      delegationManager.redeemDelegations(permissionContexts_, encodedModes_, executionCallDatas_);

        ...
    }
```

This validation is important because the delegation will only be successfully redeemed if the caller is the specified delegate or if the delegate is set to `ANY_DELEGATE`. Without this check, the payment process might fail unexpectedly when the caller (the `NativeTokenPaymentEnforcer` contract) isn't authorized as the delegate.

**Impact:** Payment transactions may revert unexpectedly

**Recommended Mitigation:** Consider adding a check to ensure that the delegate address in the allowance delegation is either `address(this)` or the special `ANY_DELEGATE` address

**Metamask:** Acknowledged. Will revert in the `DelegationManager`.

**Cyfrin:** Acknowledged.

\clearpage
