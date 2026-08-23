---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[M-01] Missing input validation on `createAuction` function parameters can
  lead to loss of value'
vuln_class: []
---

# [M-01] Missing input validation on `createAuction` function parameters can lead to loss of value

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

**Impact:**
High, as it can lead to stuck funds

**Likelihood:**
Low, as it requires user error/misconfiguration

**Description**

There are some problems with the input validation in `createAuction`, more specifically related to the timestamp values.

1. `endTimestamp` can be equal to `startTimestamp`, so `duration` will be 0
2. `endTimestamp` can be much further in the future than `startTimestamp`, so `duration` will be a huge number and the auction may never end
3. Both `startTimestamp` and `endTimestamp` can be much further in the future, so auction might never start

Those possibilities should all be mitigated, as they can lead to the initial reserves and/or the bids being stuck in the protocol forever.

**Recommendations**

Use a minimal `duration` value, for example 1 day, as well as a max value, for example 20 days. Make sure auction does not start more than X days after it has been created as well.
