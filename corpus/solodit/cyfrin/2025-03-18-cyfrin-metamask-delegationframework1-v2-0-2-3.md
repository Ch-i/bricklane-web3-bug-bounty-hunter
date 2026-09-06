---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: Parameter mismatch in `IdEnforcer::beforeHook()` event emission
vuln_class: []
---

# Parameter mismatch in `IdEnforcer::beforeHook()` event emission

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** There's a parameter ordering mismatch in the IdEnforcer contract when emitting the `UsedId` event in the `beforeHook()` function. The event declaration and the actual emission use different parameter orders for the delegator and redeemer arguments.

The event is declared with parameters in this order:

```solidity
//IdEnforcer.sol
    event UsedId(address indexed sender, address indexed delegator, address indexed redeemer, uint256 id);
// ---------
    function beforeHook( ... ) ... {
        ...
>>      emit UsedId(msg.sender, _redeemer, _delegator, id_);
    }
```

**Impact:** Incorrect event data indexing.

**Recommended Mitigation:** Consider swapping the positions of `_redeemer` and `_delegator` in the event emission to align with the event declaration.

**Metamask:** Fixed in [5f8bea9](https://github.com/MetaMask/delegation-framework/commit/5f8bea93ea2f16b48104c901c69df504355546bd)

**Cyfrin:** Resolved.
