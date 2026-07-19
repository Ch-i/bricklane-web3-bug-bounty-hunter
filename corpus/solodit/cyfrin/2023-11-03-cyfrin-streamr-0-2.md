---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Wrong validation in `DefaultUndelegationPolicy.onUndelegate()`
vuln_class: []
---

# Wrong validation in `DefaultUndelegationPolicy.onUndelegate()`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** High

**Description:** In `onUndelegate()`, it checks if the operator owner still holds at least `minimumSelfDelegationFraction` of total supply.

```solidity
   function onUndelegate(address delegator, uint amount) external {
       // limitation only applies to the operator, others can always undelegate
       if (delegator != owner) { return; }

       uint actualAmount = amount < balanceOf(owner) ? amount : balanceOf(owner); //@audit amount:DATA, balanceOf:Operator
       uint balanceAfter = balanceOf(owner) - actualAmount;
       uint totalSupplyAfter = totalSupply() - actualAmount;
       require(1 ether * balanceAfter >= totalSupplyAfter * streamrConfig.minimumSelfDelegationFraction(), "error_selfDelegationTooLow");
   }
```

But `amount` means the DATA token amount and `balanceOf(owner)` indicates the `Operator` token balance and it's impossible to compare them directly.

**Impact:** The operator owner wouldn't be able to undelegate because `onUndelegate()` works unexpectedly.

**Recommended Mitigation:** `onUndelegate()` should compare amounts after converting to the same token.

**Client:** Fixed in commit [9b8c65e](https://github.com/streamr-dev/network-contracts/commit/9b8c65ea31b6bf15fe4ec913a975782f27c0c9a0).

**Cyfrin:** Verified.
