---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-4-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[I-05] Incomplete NatSpec docs'
vuln_class: []
---

# [I-05] Incomplete NatSpec docs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

Methods have incomplete NatSpec docs, for example the `elapsedTime` method is missing the `@param timestamp` in its NatSpec, and also most methods are missing the `@return` param - for example `balancesOf` and `createAuction`. Make sure to write complete and detailed NatSpec docs for each public method.
