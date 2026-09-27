---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[M-02] Inventory costETH records max price instead of actual cost causing
  cascading errors'
vuln_class: []
---

# [M-02] Inventory costETH records max price instead of actual cost causing cascading errors

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol), [`AuctionAssist.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/AuctionAssist.sol)

**Description:**

When `_buyNFTInternal(...)` purchases an NFT, it records `costETH` as the maximum specified `value_` parameter and passes this same inflated value to `AuctionAssist`. If the marketplace refunds excess ETH, the recorded cost does not reflect the actual price paid.

```solidity
function _buyNFTInternal(...) internal {
    // ...
    // @audit Records max price before purchase executes
    _inventory[collection_][tokenId_] = InventoryRecord({
        // ...
        costETH: value_, // Max price, not actual
        // ...
    });

    // Marketplace call - may refund excess
    (bool success,) = marketplace_.call{value: value_}(marketplaceCalldata_);
    // Refund goes to receive() but costETH is never updated

    // @audit Passes same inflated value to AuctionAssist
    if (_auctionAssist != address(0)) {
        uint256 purchaseId_ = IAuctionAssist(_auctionAssist).recordPurchase(
            collection_, tokenId_, value_ // Inflated cost
        );
    }
}
```

**Impact:** The inflated `costETH` propagates through multiple calculations:

1. AuctionAssist Contributor Shares (`recordPurchase`):

   ```solidity
   uint256 shareBPS_ = (contributionAmount_ * 10000) / costETH_;
   // @audit Inflated denominator reduces contributor shares
   ```

2. Listing Prices (`_listNFTOnMarketplace`):

   ```solidity
   uint256 maxPrice_ = (costETH_ * _upperAuctionMultiplierBps) / _BPS_DENOMINATOR;
   uint256 minPrice_ = (costETH_ * _lowerAuctionMultiplierBps) / _BPS_DENOMINATOR;
   // @audit NFTs listed higher than necessary, reducing sales
   ```

3. Profit/Loss Tracking (`_processSettlement`):

   ```solidity
   bool isProfit_ = salePriceETH_ >= costETH_;
   profitOrLoss_ = isProfit_ ? salePriceETH_ - costETH_ : costETH_ - salePriceETH_;
   // @audit Profits understated, losses overstated
   ```

4. Contributor Share in Settlement (`_splitProceeds`):

   ```solidity
   uint256 contributorShareBPS_ = (totalContributions_ * 10000) / costETH_;
   // @audit Contributors receive diluted reward shares
   ```

**Recommendation:** Track actual ETH spent by measuring the balance before/after the marketplace call.

**Status:** Fixed

**Client response:** Fixed in [ffa02072c6b0c681673c8bdc44de8e810bcbeb20](https://github.com/dutch-protocol/Protocol-Contracts/commit/ffa02072c6b0c681673c8bdc44de8e810bcbeb20)
