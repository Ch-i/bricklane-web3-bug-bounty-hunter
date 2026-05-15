---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[L-01] Auction with `price == 0` can be re-created'
vuln_class: []
---

# [L-01] Auction with `price == 0` can be re-created

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

The `createAuction` method checks if auction exists with this code

```solidity
Auction storage state = _auctions[auctionId];

if (state.price != 0) {
    revert AuctionExists();
}
```

But the method does not check if the `startingOriginPrice` argument had a value of 0 - if it did, then `state.price` would be 0 in the next `createAuction` call. Even though this is not expected to happen, if it does it can lead to this line of code being executed twice:

```solidity
IERC20(reserveToken).transferFrom(msg.sender, address(this), reserveAmount);
```

which will result in a loss for the caller. Make sure to require that the value of `startingOriginPrice` is not 0.
