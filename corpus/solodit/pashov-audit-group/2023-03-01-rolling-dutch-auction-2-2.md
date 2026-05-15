---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[M-03] Protocol won''t work correctly with tokens that do not revert on failed
  `transfer`'
vuln_class: []
---

# [M-03] Protocol won't work correctly with tokens that do not revert on failed `transfer`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

**Impact:**
High, as it can lead to a loss of value

**Likelihood:**
Low, as such tokens are not so common

**Description**

Some tokens do not revert on failure in `transfer` or `transferFrom` but instead return `false` (example is [ZRX](https://etherscan.io/address/0xe41d2489571d322189246dafa5ebde1f4699f498#code)). While such tokens are technically compliant with the standard it is a common issue to forget to check the return value of the `transfer`/`transferFrom` calls. With the current code, if such a call fails but does not revert it will result in inaccurate calculations or funds stuck in the protocol.

**Recommendations**

Use OpenZeppelin's `SafeERC20` library and its `safe` methods for ERC20 transfers.
