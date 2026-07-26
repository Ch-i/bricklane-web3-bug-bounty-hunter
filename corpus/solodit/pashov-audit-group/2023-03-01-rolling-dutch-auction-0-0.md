---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[C-01] Anyone can make new bids always revert after a window expires'
vuln_class: []
---

# [C-01] Anyone can make new bids always revert after a window expires

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

**Impact:**
High, as all new bidding will revert until auction ends

**Likelihood:**
High, as anyone can execute the attack without rare preconditions

**Description**

The `fulfillWindow` method is a `public` method that is also called internally. It sets `window.processed` to `true`, which makes it callable only once for a single `windowId`. The problem is that the `commitBid` function has the following logic:

```solidity
if (hasExpired) {
    window = _window[auctionId][windowExpiration(auctionId)];
}
```

Where `windowExpiration` calls `fulfillWindow` with the latest `windowId` in itself. If any user manages to call `fulfillWindow` externally first, then the `window.processed` will be set to `true`, making the following check in `fulfillWindow`

```solidity
if (window.processed) {
    revert WindowFulfilled();
}
```

revert on every `commitBid` call from now on. This will result in inability for anyone to place more bids, so the auction will not sell anything more until the end of the auction period.

**Recommendations**

Make `fulfillWindow` to be `internal` and then add a new public method that calls it internally but also has the `inactiveAuction` modifier as well - this way anyone will be able to complete a window when an auction is finished even though no one can call `commitBid`.
