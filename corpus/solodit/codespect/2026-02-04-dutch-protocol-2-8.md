---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-8
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[L-09] record.listed status is not updated after the NFT is sold'
vuln_class: []
---

# [L-09] record.listed status is not updated after the NFT is sold

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol)

**Description:**

After the vault's listed NFT is purchased contract doesn't update the `_inventory[collection_][tokenId_].listed` status to false, although it's not listed anymore. This will cause `DutchVault` being unable to list previously sold NFTs again because of following check in `listNFTOnMarketplace(...)`:

```solidity
if (record_.listed) {
    revert NFTAlreadyListed();
}
```

**Impact:** `DutchVault` can't list previously sold NFTs again.

**Recommendation:** Set `_inventory[collection_][tokenId_].listed` to false after NFT got purchased.

**Status:** Fixed

**Client response:** Fixed in [26db416a8d185792721a1da1f9622eb8252f7838](https://github.com/dutch-protocol/Protocol-Contracts/commit/26db416a8d185792721a1da1f9622eb8252f7838)
