---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[M-02] Loss of precision in `scalarPrice` function'
vuln_class: []
---

# [M-02] Loss of precision in `scalarPrice` function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

**Impact:**
Medium, as the price will not be very far from the expected one

**Likelihood:**
Medium, as it will not always result in big loss of precision

**Description**

In `scalarPrice` there is this code:

```solidity
uint256 b_18 = 1e18;
uint256 t_mod = t % (t_r - t);
uint256 x = (t + t_mod) * b_18 / t_r;
uint256 y = !isInitialised ? state.price : window.price;

return y - (y * x) / b_18;
```

Here, when you calculate `x` you divide by `t_r` even though later you multiply `x` by `y`. To minimize loss of precision you should always do multiplications before divisions, since Solidity just rounds down when there is a remainder in the division operation.

**Recommendations**

Always do multiplications before divisions in Solidity, make sure to follow this throughout the whole `scalarPrice` method.
