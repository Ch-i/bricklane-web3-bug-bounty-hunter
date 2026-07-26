---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-4-0
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
title: '[I-01] Using `require` statements without error strings'
vuln_class: []
---

# [I-01] Using `require` statements without error strings

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

The `activeAuction` and `inactiveAuction` modifiers use `require` statements without error strings. Use `if` statements with custom errors instead for a better error case UX.
