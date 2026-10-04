---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-4
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
title: '[L-05] It’s possible to create duplicate listings in DutchAuctionMarketplace'
vuln_class: []
---

# [L-05] It’s possible to create duplicate listings in DutchAuctionMarketplace

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchAuctionMarketplace.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchAuctionMarketplace.sol)

**Description:**

The `_createListing(...)` function doesn't check if the `tokenId_` of the `nftContract_` is currently listed or not and lets users to create duplicate listings, which will remain in the marketplace even after the NFT will be sold.

**Impact:** This will cause gas griefing on users that will try to purchase the NFT using duplicate listings.

**Recommendation:** Check if the NFT is already listed in the `DutchAuctionMarketplace`.

**Status:** Fixed

**Client response:** Fixed in [28b610ddfda26c7d47f0915e79de67ed57b2bb53](https://github.com/dutch-protocol/Protocol-Contracts/commit/28b610ddfda26c7d47f0915e79de67ed57b2bb53)
