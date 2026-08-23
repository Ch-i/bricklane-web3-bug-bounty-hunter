---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Collector can add `CreatorStory`, corrupting the provenance of an artwork
vuln_class: []
---

# Collector can add `CreatorStory`, corrupting the provenance of an artwork

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** The purpose of the `IStory` interface is to allow 3 different entities (Admin, Creator and Collectors) to add "Stories" about a given artwork (NFT) which [describes the provenance of the artwork](https://docs.transientlabs.xyz/tl-creator-contracts/common-features/story-inscriptions). In the art world the "provenance" of an item can affect its status and price, so the `IStory` interface aims to facilitate an on-chain record of an artwork's "provenance".

`IStory` is designed to work like this:
* Creator/Admin can add a `CollectionsStory` for when a collection is added to a contract
* Creator of an artwork can add a `CreatorStory`
* Collector of an artwork can add one or more `Story` about their experience while holding the artwork

The `IStory` interface specification requires that `addCreatorStory` is only called by the creator:
```solidity
/// @notice Function to let the creator add a story to any token they have created
/// @dev This function MUST implement logic to restrict access to only the creator
function addCreatorStory(uint256 tokenId, string calldata creatorName, string calldata story) external;
```

But in the CryptoArt implementation of the `IStory` interface, the current token owner can always emit `CreatorStory` events:
```solidity
function addCreatorStory(uint256 tokenId, string calldata, /*creatorName*/ string calldata story)
    external
    onlyTokenOwner(tokenId)
{
    emit CreatorStory(tokenId, msg.sender, msg.sender.toHexString(), story);
}
```

**Impact:** As an NFT is sold or transferred to new owners, each subsequent owner can continue to add new `CreatorStory` events even though they aren't the Creator of the artwork. This corrupts the provenance of the artwork by allowing Collectors to add to the `CreatorStory` as if they were the Creator.

**Recommended Mitigation:** Only the Creator of an artwork should be able to emit the `CreatorStory` event. Currently the on-chain protocol does not record the address of the creator; this could either be added or `onlyOwner` could be used where the contract owner acts as a proxy for the creator.

**CryptoArt:**
Fixed in commit [94bfc1b](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/94bfc1b1454e783ef1fb9627cfaf0328ebe17b47#diff-1c61f2d0e364fa26a4245d1033cdf73f09117fbee360a672a3cb98bc0eef02adL439-R439).

**Cyfrin:** Verified.

\clearpage
