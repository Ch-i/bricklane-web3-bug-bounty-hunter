---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[L-03] The `scalarPrice` method should have an `activeAuction` modifier'
vuln_class: []
---

# [L-03] The `scalarPrice` method should have an `activeAuction` modifier

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

If an auction is inactive then the `scalarPrice` method will still be returning a price, even though it should not, since auction is over. Add the `activeAuction` modifier to it.
