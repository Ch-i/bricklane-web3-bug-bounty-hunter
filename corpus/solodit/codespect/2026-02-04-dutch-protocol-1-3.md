---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-1-3
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
title: '[M-04] Stuck NFTs block rebalancing and write-off workaround causes contributor
  reward loss'
vuln_class: []
---

# [M-04] Stuck NFTs block rebalancing and write-off workaround causes contributor reward loss

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol)

**Description:**

The `_rebalanceCollections(...)` function prevents removing any collection that still holds NFTs. If a collection has even one NFT in inventory, it cannot be removed from the allocation list.

```solidity
function _rebalanceCollections(...) internal {
    // Mark new collections temporarily using max value.
    for (uint256 i; i < collections_.length; ++i) {
        _allocations[collections_[i]] = type(uint16).max;
    }

    for (uint256 i; i < _collectionList.length; ++i) {
        address oldCollection_ = _collectionList[i];

        // @audit If ANY collection being removed has NFTs, entire rebalance reverts
        if (
            _allocations[oldCollection_] != type(uint16).max
                && _itemsHeld[oldCollection_] > 0
        ) {
            revert CollectionHasNFTs();
        }
        // ...
    }
}
```

If an NFT becomes unsellable (marketplace delists it, collection rugpulls, floor price crashes, legal issues), that collection can never be removed from allocations. This blocks ALL rebalancing operations for the entire vault.

**Workaround causes contributor loss:** The owner can call `recordSettlement(collection, tokenId, 0, 0)` to manually "settle" a stuck NFT at zero price. However, this causes real fund loss:

1. Contributor reward loss: If `AuctionAssist` contributors funded the NFT purchase with ETH, settling at 0 means `salePriceDUTCH_ = 0`, so contributors receive 0 DUTCH rewards despite funding the purchase;
2. Vault retains asset: The vault still physically holds the NFT (which may have value), but contributors get nothing;
3. Inflated losses: Full `costETH` is recorded as realized loss, overstating the protocol's trading losses;
4. No recovery path: If the NFT is later sold through other means, there's no mechanism to credit contributors retroactively.

**Impact:** This can prevent rebalancing from being possible. And the workaround causes the vault to incur total loss of the asset.

**Recommendation:** Add a dedicated `writeOffNFT(...)` function that cleanly handles stuck inventory.

**Status:** Fixed

**Client response:** Fixed in commit [f88609069273aeb2cbb8df62dcd950018da95d21](https://github.com/dutch-protocol/Protocol-Contracts/commit/f88609069273aeb2cbb8df62dcd950018da95d21)
