---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[H-01] Users are likely to lose their bid if `purchaseToken` is a low-decimals
  token'
vuln_class: []
---

# [H-01] Users are likely to lose their bid if `purchaseToken` is a low-decimals token

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

**Impact:**
High, because users will lose their entire bid amount

**Likelihood:**
Medium, because it happens when `purchaseToken` is a low-decimals token, but those are commonly used

**Description**

When a user calls `commitBid` he provides a `volume` parameter, which is the amount of `purchaseToken` he will bid, and a `price` parameter, which is the price in `reserveToken`. His bid is then cached and when window expires the `fulfillWindow` method is called, where we have this logic:

```solidity
_auctions[auctionId].reserves -= volume / price;
_auctions[auctionId].proceeds += volume;

_claims[bidder][auctionId] = abi.encode(refund - volume, claim + (volume / price));
```

The problem lies in the `volume / price` calculation. In the case that the `reserveToken` is a 18 decimal token (most common ones) but the `purchaseToken` has a low decimals count - `USDC`, `USDT` and `WBTC` have 6 to 8 decimals, then it's very likely that the `volume / price` calculation will result in rounding down to 0. This means that the auction owner would still get the whole bid amount, but the bidder will get 0 `reserveToken`s to claim, resulting in a total loss of his bid.

The issue is also present when you are using same decimals tokens for both `reserve` and `purchase` tokens but the `volume` in a bid is less than the `price`. Again, the division will round down to zero, resulting in a 100% loss for the bidder.

**Recommendations**

In `commitBid` enforce that `volume >= price` and in `createAuction` enforce that the `reserveToken` decimals are equal to the `purchaseToken` decimals.
