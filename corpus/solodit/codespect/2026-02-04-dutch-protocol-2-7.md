---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-7
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[L-08] _buyNFTInternal(...) function uses unchecked calldata for NFT purchases'
vuln_class: []
---

# [L-08] _buyNFTInternal(...) function uses unchecked calldata for NFT purchases

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol)

**Description:**

The `_buyNFTInternal(...)` function receives arbitrary calldata and uses it to purchase NFTs from the marketplaces:

```solidity
(bool success,) =
    marketplace_.call{value: value_}(marketplaceCalldata_);
if (!success) revert MarketplaceCallFailed();
```

The function doesn't validate the arbitrary calldata, which means that any function with any parameters can be called on approved marketplaces. Attack scenario:

1. Attacker waits for approved collection's `getMaxPriceForCollection(...)` to be high enough or an NFT listed below the floor price to pass the `value_ > this.getMaxPriceForCollection(collection_)` check;
2. Calls marketplace function that batch buys NFTs;
3. Besides purchasing the NFT for the vault from approved collection, attacker also buys unvalued NFT that he listed on the marketplace.

**Impact:** Attacker can profit by making the vault buy unvalued NFTs.

**Recommendation:** Validate `marketplaceCalldata_` parameter.

**Status:** Fixed

**Client response:** Fixed in commit [5dd04c73343a03b823f6b1037dc52d60696bb620](https://github.com/dutch-protocol/Protocol-Contracts/commit/5dd04c73343a03b823f6b1037dc52d60696bb620)

**CODESPECT fix review:** Since the unverified calldata may still potentially expand the attack surface, we still recommend using a `(market address => (function signature => bool))` mapping to further restrict callable functions and reduce attack risks.

**Client response:** Fixed in [PR-125](https://github.com/dutch-protocol/Protocol-Contracts/pull/125). We changed the marketplace address allowlist to `[address, selector]` allowlist.
