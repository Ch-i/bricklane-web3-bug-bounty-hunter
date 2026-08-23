---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-stakedao-onlyboost-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md
tags:
- firm:zachobront
- report:2023-11-01-stakedao-onlyboost
title: '[L-01] Optimizer rounds negative feeDiff values to zero'
vuln_class: []
---

# [L-01] Optimizer rounds negative feeDiff values to zero

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-StakeDAO-Onlyboost.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md)_

---

In the optimal deposit formula in Optimizer.sol, we calculate the `feeDiff` between Convex and StakeDAO. `feeDiff` represents how much more profitable each dollar earned in Convex is than StakeDAO, taking into account fees and incentives.

Since StakeDAO's fee is 16% and Convex is 17%, and we are only taking into account Convex incentives, the possible range for `feeDiff` is `-1 <= feeDiff <= inf`.

When this value is calculated, we do the following:
```solidity
uint256 feeDiff = boost + stakeDaoTotalFee > convexTotalFee ? stakeDaoTotalFee + boost - convexTotalFee : 0;
```
In short, if `boost` (Convex incentives) is greater than the gap in fees, we perform the calculation. However, if `boost` is not sufficient to cover the gap in fees, we default to zero.

This creates a loss of precision in the formula for situations when Convex's incentive is less than 1%, which is due to happen in the coming years as their inflation rate slows down.

**Recommendation**

To increase the precision, allow `feeDiff` to represent a negative number as low as `-1e16` and use that value in the computation.

**Review**

Acknowledged.
