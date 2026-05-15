---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-tokendistributor-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-TokenDistributor.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-tokendistributor
title: '[M-01] DoS attack on initialization is possible'
vuln_class: []
---

# [M-01] DoS attack on initialization is possible

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-TokenDistributor.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-TokenDistributor.md)_

---

**Severity**

**Impact:**
High, as the initialization can be blocked

**Likelihood:**
Low, as it a front-running type of an attack with no benefit for the attacker

**Description**

The `initializeDistributor` method in `TokenDistributor` has the following check:

```solidity
require(token.balanceOf(address(this)) == _totalTokensToDistribute, "totalTokensToDistribute must match token balance of contract");
```

This gives the expectation that the owner will pre-transfer let's say 10 tokens to the contract and then set the `_totalTokensToDistribute` argument to 10 when calling `initializeDistributor`. The problem with this is that if a malicious user front-runs the owner call with a transfer of 1 wei worth of `token` to the contract, the check and the transaction will revert as the balance will not be equal anymore.

**Recommendations**

Change the code in the following way:

```diff
- require(
-    token.balanceOf(address(this)) == _totalTokensToDistribute,
-    "totalTokensToDistribute must match token balance of contract"
- );
+ token.safeTransferFrom(msg.sender, address(this), _totalTokensToDistribute);
```

and do not pre-transfer tokens to the contract.
