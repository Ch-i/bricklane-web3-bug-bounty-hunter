---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-4-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[I-06] Missing `override` keyword'
vuln_class: []
---

# [I-06] Missing `override` keyword

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

The `createAuction`, `withdraw` and `redeem` methods are missing the `override` keyword even though the override methods from the `IRDA` interface. Add it to the mentioned methods.
