---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-2
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
title: '[L-03] Fake NFT contract attack due to missing ownership verification'
vuln_class: []
---

# [L-03] Fake NFT contract attack due to missing ownership verification

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchAuctionMarketplace.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchAuctionMarketplace.sol#L1013)

**Description:**

The `_settleInternal(...)` function transfers an NFT from the seller to the buyer when an auction is settled. After calling `transferFrom(...)` on the NFT contract, the function burns the buyer's DUTCH tokens as payment.

```solidity
function _settleInternal(...) internal {
    // ...
    // @audit no ownership verification after transfer
    IERC721(listing_.nftContract).transferFrom(
        listing_.seller, buyer_, listing_.tokenId
    );

    // Buyer's DUTCH tokens are burned regardless of transfer success
    _DUTCH.burn(buyer_, listing_.currentPrice);
    // ...
}
```

However, there is no verification that the NFT transfer actually succeeded.

**Impact:** A malicious seller can deploy a fake ERC721 contract with a `transferFrom(...)` function that always returns success but never actually transfers any tokens. When a victim bids on this fake NFT listing:

1. The attacker creates a listing with their fake NFT contract;
2. The victim places a bid on what appears to be a legitimate NFT;
3. On settlement, the fake `transferFrom(...)` succeeds but transfers nothing;
4. The victim's DUTCH tokens are burned as payment;
5. The attacker receives the payment while the victim receives nothing.

This results in a complete loss of the buyer's DUTCH tokens with no recourse.

**Recommendation:** Add ownership verification after the transfer:

```solidity
IERC721(listing_.nftContract).transferFrom(
    listing_.seller, buyer_, listing_.tokenId
);

require(
    IERC721(listing_.nftContract).ownerOf(listing_.tokenId) == buyer_,
    "NFT transfer failed"
);
```

**Status:** Fixed

**Client response:** Fixed in [7b9105de3aaeb5808a76caeb75ef0016bc9777b1](https://github.com/dutch-protocol/Protocol-Contracts/commit/7b9105de3aaeb5808a76caeb75ef0016bc9777b1)
