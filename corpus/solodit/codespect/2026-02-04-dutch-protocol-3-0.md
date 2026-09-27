---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-3-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[I-01] Improper collection configuration checks'
vuln_class: []
---

# [I-01] Improper collection configuration checks

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`AuctionAssist.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/AuctionAssist.sol#L259)

**Description:**

In the `contribute(...)` function, the collection configuration is checked by verifying whether `basePrice_` is zero.

```solidity
function contribute(...) external payable nonReentrant whenNotPaused{
    //...
    // 2. Get base price (target price) from DutchVault.
    uint256 basePrice_ = IDutchVault(_dutchVault).getBasePrice(collection_);

    // 3. Validate collection is configured.
    if (basePrice_ == 0) {
        revert CollectionNotConfigured();
    }
    //...
}
```

However, when a collection is removed, `basePrice_` may not be cleared.

**Impact:** This may cause users to mistakenly deposit into an inactive collection.

**Recommendation:** It is recommended to check that `_allocations[collection_]` is not equal to zero.

**Status:** Fixed

**Client response:** Fixed in [e38f1cd269761bb4b5901c321cedb83b2eab515e](https://github.com/dutch-protocol/Protocol-Contracts/commit/e38f1cd269761bb4b5901c321cedb83b2eab515e)
