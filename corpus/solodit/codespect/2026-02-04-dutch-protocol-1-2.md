---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-1-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[M-03] Marketplace refunds misattributed across collections causing contributor
  reward loss'
vuln_class: []
---

# [M-03] Marketplace refunds misattributed across collections causing contributor reward loss

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol)

**Description:**

When `_buyNFTInternal(...)` purchases an NFT, it deducts the full specified `value_` from the target collection's balance before executing the marketplace call. If the actual purchase price is less than `value_`, the marketplace refunds the excess ETH to the vault.

```solidity
function _buyNFTInternal(...) internal {
    // ...
    // Full value deducted from specific collection
    _collectionBalances[collection_] -= value_;

    // Marketplace call - may refund excess
    (bool success,) = marketplace_.call{value: value_}(marketplaceCalldata_);
    // ...
}
```

The refund arrives at the vault's `receive()` function, which distributes incoming ETH proportionally across ALL collections based on their allocation percentages:

```solidity
receive() external payable {
    // ...
    for (uint256 i; i < _collectionList.length; ++i) {
        address collection_ = _collectionList[i];
        uint16 allocation_ = _allocations[collection_];
        uint256 share_ = (msg.value * allocation_) / _BPS_DENOMINATOR;
        _collectionBalances[collection_] += share_; // All collections receive share
    }
    // ...
}
```

**Impact:** Contributors who funded Collection A through `AuctionAssist` receive reduced rewards because their collection's balance is understated. Meanwhile, Collection B contributors receive unearned gains. Over multiple purchases with refunds, this drift accumulates, causing systematic unfairness to active collection contributors.

**Recommendation:** Track the actual ETH spent and credit any refund back to the originating collection.

**Status:** Acknowledged

**Client response:** Issue fixed: [a970cba006ae1bbc0145015bd7b8495d47d359e5](https://github.com/dutch-protocol/Protocol-Contracts/commit/a970cba006ae1bbc0145015bd7b8495d47d359e5)

**CODESPECT fix review:** This fix is incorrect and may lead to double accounting. For example:

1. The vault sends 1 ETH to `marketplace_` (`value = 1 ETH`);
2. Purchasing the NFT costs 0.95 ETH, with a 0.05 ETH refund;
3. The refund triggers the `receive` function, which distributes it across collections;
4. After the call completes, `collectionBalances[collection_]` records an additional 0.05 ETH refund again.

**Client response:** I think for simplicity, we are fine with redistributing the refund across all collections. The refund will be small and in many cases, there will be no refund at all. Fixed in: [PR-126](https://github.com/dutch-protocol/Protocol-Contracts/pull/126)
