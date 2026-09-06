---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[C-03] The logic in `elapsedTime` is flawed'
vuln_class: []
---

# [C-03] The logic in `elapsedTime` is flawed

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

**Impact:**
High, as the method is used to calculate the price of the auction but will give out wrong results

**Likelihood:**
High, as the problems are present almost all of the time during an auction

**Description**

There are multiple flaws with the `elapsedTime` method:

1. If there are 0 windows, the `windowIndex` variable (which is used for the windows count) will be 1, which is wrong and will lead to a big value for `windowElapsedTime` when it should be 0
2. If `auctionElapsedTime == windowElapsedTime` we will get `auctionElapsedTime` as a result, but if there was just 1 more second in `auctionElapsedTime` we would get `auctionElapsedTime - windowElapsedTime` which would be 1 as a result, so totally different result
3. When a window is active, the `timestamp` argument will have the same value as the `auction.startTimestamp` so `auctionElapsedTime` will always be 0 in this case

The method has multiple flaws and works only in the happy-case scenario.

**Recommendations**

Remove the method altogether or extract two methods out of it, removing the `timestamp` parameter to simplify the logic. Also think about the edge case scenarios.
