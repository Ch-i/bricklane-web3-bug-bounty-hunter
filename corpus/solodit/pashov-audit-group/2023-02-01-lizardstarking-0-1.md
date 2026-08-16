---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[C-02] Calculation for `owedAmount` will round down to zero'
vuln_class: []
---

# [C-02] Calculation for `owedAmount` will round down to zero

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

**Impact:**
High, as this will result in 0 claimable rewards for users when they should have been able to claim some

**Likelihood:**
High, as this will happen any time the user's share is smaller than the pool's cached global share, which is almost always

**Description**

The `claimCalculation` method calculates the `owedAmount` that is about to be send to the user in the form of `USDC` rewards with the following calculation:

```solidity
owedAmount = (currentShareRaw / pool[_poolNumber].currentGlobalShare) * pool[_poolNumber].value;
```

This happens both if the `_poolNumber == 1` and if it is a different value, but the code is present in both cases. The issue is that it does division before multiplication, where if the `pool[_poolNumber].currentGlobalShare` value is bigger than the `currentShareRaw` value, the division will round down to zero resulting in zero `owedAmount`. This will almost always happen as it is expected that the pool's cached `currentGlobalShare` will be bigger than a single user's raw share. This means that no matter how much a user waits he won't be able to claim his rewards for this pool, leaving them stuck in the contract forever.

This issue was partly noticed by the developer mid-audit, where he fixed one of the places where `owedAmount` was calculated, but the other `owedAmount` calculation error one wasn't discovered.

**Recommendations**

Change the code in the following way:

```diff
- owedAmount = (currentShareRaw / pool[_poolNumber].currentGlobalShare) * pool[_poolNumber].value;
+ owedAmount = currentShareRaw * pool[_poolNumber].value / pool[_poolNumber].currentGlobalShare;
```

So this way you do multiplication before division which will not round down to zero, as the pool's value is in `USDC` that has 6 decimals, but the shares have 18 decimals.
