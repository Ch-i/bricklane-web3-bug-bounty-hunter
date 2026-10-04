---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-3-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[I-03] The price growth has no upper limit'
vuln_class: []
---

# [I-03] The price growth has no upper limit

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol#L651)

**Description:**

If `_buyIncrements[collection_]` is configured, the price the protocol can pay for an NFT will increase over time until an NFT in the collection is purchased, at which point it resets.

```solidity
function getMaxPriceForCollection(address collection_)
    external
    view
    returns (uint256 maxPrice_)
{
    //...
    uint256 timeBuffer_ =
        (blocksSinceLastBuy_ + 1) * _buyIncrements[collection_];
    return basePrice_ + timeBuffer_;
}
```

If NFTs are never purchased, the price will continue to rise without any upper limit.

**Impact:** If a collection continuously has no NFT purchases due to no NFTs being listed, the protocol's bid could become far higher than the funds raised.

**Recommendation:** It is recommended to set a limit on price growth.

**Status:** Acknowledged

**Client response:** We acknowledge this finding, but consider the current implementation intentional and safe by design.

The `getMaxPriceForCollection` function represents the protocol's maximum willingness to pay (a market signal), not a guarantee of payment capability. While this value can grow unbounded over time, actual purchases in `_buyNFTInternal` are protected by a critical balance check (`if (_collectionBalances[collection_] < value_) revert InsufficientBalanceForPurchase();`) that ensures the protocol can never spend more than it has, regardless of how high `getMaxPriceForCollection` grows. The unbounded growth in willingness to pay is intentional, and we believe the market should determine pricing without artificial protocol-imposed limits. The real constraint (available treasury funds) is what matters, not an artificial cap on willingness to pay. If `getMaxPriceForCollection` grows beyond available funds, purchases will simply fail until more funds are deposited or the price resets via a purchase, and the protocol owner can always adjust `_buyIncrements[collection_]` or reset `_lastBuyBlock[collection_]` if needed.
