---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-25-hyperwave-corewriter-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md
tags:
- firm:codespect
- report:2025-08-25-hyperwave-corewriter
title: '[I-02] Replace storage writes with memory ones'
vuln_class: []
---

# [I-02] Replace storage writes with memory ones

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-25-Hyperwave-CoreWriter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md)_

---

**Files:** [`TradeStakeManager.sol`](https://github.com/SwellNetwork/hlp-corewriter/blob/5a19bb4373eaf3eb57d872f81d20177fb5cf9b2b/src/TradeStakeManager.sol#L103)

**Description:**

Whenever the bounds for native or other tokens are queried, they are assigned to a variable declared as `storage`, e.g.:

```solidity
PriceBounds storage bounds; // @audit Is storage necessary here?
if (requestedNative) {
    spotWhitelisted = _getNativeSpotWhitelist(account);
    bounds = _getNativePriceBounds();
} else {
    spotWhitelisted = _getTokenSpotWhitelist(account, tokenAddress);
    bounds = _getTokenPriceBounds(tokenAddress);
}
```

The `_getTokenPriceBounds(...)` function returns a storage variable. However, in functions such as `placeSellSpotOrder(...)` or `placeBuySpotOrder(...)`, the bounds are only read, not modified. Using `storage` in these cases is unnecessary and increases gas usage. A getter returning a memory copy of the bounds would be more efficient.

**Impact:** Minor gas optimisation; limited effect due to the use of Hyperliquid.

**Recommendation:** Introduce getter functions that return the bounds as `memory` when only reading data, avoiding unnecessary storage references.

**Status:** Acknowledged

**Client response:** We acknowledge and choose not to change, since the benefits are eroded by copying unused fields from storage.
