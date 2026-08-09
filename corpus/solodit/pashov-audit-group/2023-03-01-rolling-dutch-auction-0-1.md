---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-1
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
title: '[C-02] Successful bidders can lose significant value due to division rounding'
vuln_class: []
---

# [C-02] Successful bidders can lose significant value due to division rounding

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

**Impact:**
High, as possibly significant value will be lost

**Likelihood:**
High, as it will happen with most bids

**Description**

The `fulfillWindow` method calculates the auction reserves and proceeds after a successful bid in a window. Here is how it accounts it in both the `auctions` and `claims` storage mappings:

```solidity
_auctions[auctionId].reserves -= volume / price;
_auctions[auctionId].proceeds += volume;

_claims[bidder][auctionId] = abi.encode(refund - volume, claim + (volume / price));
```

The problem is in the `volume / price` division and the way Solidity works - since it only has integers, in division the result is always rounded down. This would mean the bidder will have less `claim` tokens than expected, while the `_auctions[auctionId].reserves` will keep more tokens than it should have. Let's look at the following scenario:

1. The `reserve` token is `WETH` (18 decimals) and the purchase token is `DAI` - 18 decimals as well
2. Highest bidder in the window bid 2 \* 1e18 - 1 `DAI` with a price of 1e18 `WETH`
3. While the bid should have resulted in 1.99999 `WETH` bought, the user will receive only 1 `WETH` but not get a refund here
4. The user got the same amount of `WETH` as if he bid 1e18 but he bid twice as much, minus one

Every remainder of the `volume / price` division will result in a loss for the bidder.

**Recommendations**

Design the code so that the remainder of the `volume / price` division gets refunded to the bidder, for example adding it to the `refund` value.
