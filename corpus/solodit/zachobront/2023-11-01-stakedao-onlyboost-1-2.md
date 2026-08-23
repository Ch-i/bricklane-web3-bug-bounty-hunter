---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-stakedao-onlyboost-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md
tags:
- firm:zachobront
- report:2023-11-01-stakedao-onlyboost
title: '[M-03] Optimizer will misallocate when StakeDAO is above full boost'
vuln_class: []
---

# [M-03] Optimizer will misallocate when StakeDAO is above full boost

_Section severity (from Solodit section header): Medium_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-StakeDAO-Onlyboost.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md)_

---

On Page 5 of the whitepaper, it says:

> We can assume that when this balance is reached for a given gauge, neither Convex nor Stake DAO have maximum boost, which enables us to get rid of the min formula.

The `min` in the formula is intended to cap the boost at 2.5x. If the proportion of veCRV held by a user is greater than their proportion of pool tokens, they will be capped at 2.5x, rather than further increasing the boost.

One example of when this could happen is if both pools have full 2.5x boosts. This example was pointed out in the last audit, and a fix was added to manually send funds to Convex if both pools had maximum boosts.

However, upon further reflection, this fix is not sufficient.

We can simplify the issue with the understanding that, when the `min` is removed from the formula, it allows the formula's perceived boost for a protocol to exceed 2.5x. For example, if StakeDAO holds `10%` of veCRV and only holds `1%` of a given pool, assuming the pool has 100 tokens for simplicity, the boost will be calculated as:
```python
boost = ((0.4 * 1) + (0.6 * 100 * 10%)) / 0.4 = 16x
```
If the min was included, it would have been capped at 2.5x, but instead is allowed to reach 16x. As a result, when the Optimizer calculates the ideal allocation, it will favor this pool more aggressively than it should.

The issue pointed out in the previous audit examines when such an example is matched with a Convex pool at full boost. In this case, the 2.5x from Convex is identical to the 2.5x from StakeDAO, and the Optimizer misattributing StakeDAO a 16x boost would cause funds to flow there, even though the ideal would be allocate to Convex due to the incentives.

But, as we can see from this example, the same issue holds when Convex reaches 2.49x boost, and lower. In fact, calculating precisely, we find the breakeven point. The returns from each protocol are as follows:
```python
convex _return= convex_boost * (1 - 0.17 + 0.05)
sd_return = sd_boost * (1 - 0.16)
```
To calculate the breakeven point for `convex_boost` for when `sd_boost == 2.5x`, we can solve and plug in:
```python
convex_boost * 0.88 == 2.5 * 0.84
convex_boost = 2.386
```
Therefore, in any situation in which Convex has a boost greater than 2.386, it is preferable over StakeDAO with full boost. In these cases, Convex should receive the full deposit.

The same issue exists when Convex is below 2.386x boost, because the optimal balance for StakeDAO will be set too high, so more funds will flow to StakeDAO than should.

**Recommendation**

The issue that the Optimizer assumes that boosts can get arbitrarily high can't be accurately solved by intercepting the request for special circumstances beforehand, because any situation in which StakeDAO has more than 2.5x boost will create an inaccurate optimal value.

Instead, the `computeOptimalDepositAmount()` formula should take the minimum amounts into account when performing its calculations to get a more accurate response.

**Review**

Acknowledged.
