---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-0
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
title: '[L-01] Bad ownership check will prevent DutchVault from buying NFTs that were
  purchased in the past'
vuln_class: []
---

# [L-01] Bad ownership check will prevent DutchVault from buying NFTs that were purchased in the past

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol)

**Description:**

The `_buyNFTInternal(...)` function performs following NFT ownership check:

```solidity
InventoryRecord storage existing_ = _inventory[collection_][tokenId_];
if (existing_.costETH > 0) {
    revert NFTAlreadyOwned();
}
```

This will cause `DutchVault` being unable to buy back and sell NFTs that were purchased in the past because of the previously created `_inventory[collection_][tokenId_]` record. The check also creates attack surface by transfering NFT directly to the contract or making the `DutchVault` to purchase the NFT for free.

**Impact:** Vault will be unable to buy the same NFT again.

**Recommendation:** The check should look like this:

```solidity
if (IERC721(collection_).ownerOf(tokenId_) == address(this)) {
    revert NFTAlreadyOwned();
}
```

**Status:** Fixed

**Client response:** It is now possible to buy the same NFT multiple times [2346c1e0379cba853a153f9914a0011ea07b84af](https://github.com/dutch-protocol/Protocol-Contracts/commit/2346c1e0379cba853a153f9914a0011ea07b84af)
