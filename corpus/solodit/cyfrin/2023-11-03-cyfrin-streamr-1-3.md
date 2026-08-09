---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: In `Operator._transfer()`, `onDelegate()` should be called after updating the
  token balances
vuln_class: []
---

# In `Operator._transfer()`, `onDelegate()` should be called after updating the token balances

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** Medium

**Description:** In `_transfer()`, `onDelegate()` is called to validate the owner's `minimumSelfDelegationFraction` requirement.

```solidity
File: contracts\OperatorTokenomics\Operator.sol
324:         // transfer creates a new delegator: check if the delegation policy allows this "delegation"
325:         if (balanceOf(to) == 0) {
326:             if (address(delegationPolicy) != address(0)) {
327:                 moduleCall(address(delegationPolicy), abi.encodeWithSelector(delegationPolicy.onDelegate.selector, to)); //@audit
should be called after _transfer()
328:             }
329:         }
330:
331:         super._transfer(from, to, amount);
332:
```

But `onDelegate()` is called before updating the token balances and the below scenario would be possible.

- The operator owner has 100 shares(required minimum fraction). And there are no undelegation policies.
- Logically, the owner shouldn't be able to transfer his 100 shares to a new delegator due to the min fraction requirement in `onDelegate()`.
- But if the owner calls `transfer(owner, to, 100)`, `balanceOf(owner)` will be 100 in `onDelegation()` and it will pass the requirement because it's called before `super._transfer()`.

**Impact:** The operator owner might transfer his shares to other delegators in anticipation of slashing, to avoid slashing.

**Recommended Mitigation:** `onDelegate()` should be called after `super._transfer()`.

**Client:** Fixed in commit [93d6105](https://github.com/streamr-dev/network-contracts/commit/93d610561c109058c967d1d2f49ea91811f28579).

**Cyfrin:** Verified.
