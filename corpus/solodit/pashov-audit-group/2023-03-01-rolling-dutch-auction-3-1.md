---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[L-02] The `commitBid` method does not follow Checks-Effects-Interactions
  pattern'
vuln_class: []
---

# [L-02] The `commitBid` method does not follow Checks-Effects-Interactions pattern

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

It's a best practice to follow the CEI pattern in methods that do value transfers. Still, it is not always the best solution, as ERC777 tokens can still reenter while the contract is in a strange state even if you follow CEI. I would recommend adding a `nonReentrant` modifier to `commitBid` and also moving the `transferFrom` call to the end of the method.
