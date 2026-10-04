---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-3-3
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
title: '[I-04] _lastBuyBlock is not fully updated'
vuln_class: []
---

# [I-04] _lastBuyBlock is not fully updated

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol#L499)

**Description:**

`_lastBuyBlock` stores the last purchase block for each collection. The protocol allows the maximum price for purchasing NFTs from that collection to increase over the elapsed blocks. When calling the `setCollectionAllocations(...)` function to update collections, only collections with `_lastBuyBlock` equal to 0 will have their `_lastBuyBlock` updated.

```solidity
function setCollectionAllocations(...) external onlyOwner whenNotPaused {
    //...
    for (uint256 i; i < collections_.length; ++i) {
        _allocations[collections_[i]] = allocationsBPS_[i];
        _collectionList.push(collections_[i]);

        // Initialize lastBuyBlock if not set (prevents huge first-buy cap).
        if (_lastBuyBlock[collections_[i]] == 0) {
            _lastBuyBlock[collections_[i]] = block.number;
        }

        emit AllocationUpdated(collections_[i], allocationsBPS_[i]);
    }
}
```

However, if a collection was previously removed and then added again, its `_lastBuyBlock` will not be 0, so `_lastBuyBlock` will not be updated when it is re-added.

**Impact:** If too much time has passed since `_lastBuyBlock`, the payable price for the collection could become excessively high.

**Recommendation:** It is recommended to update `_lastBuyBlock` for each collection when calling `setCollectionAllocations(...)`.

**Status:** Fixed

**Client response:** Fixed in [f6c7c3e0a42e80ff2cb0d147854a96113a6c276b](https://github.com/dutch-protocol/Protocol-Contracts/commit/f6c7c3e0a42e80ff2cb0d147854a96113a6c276b)
