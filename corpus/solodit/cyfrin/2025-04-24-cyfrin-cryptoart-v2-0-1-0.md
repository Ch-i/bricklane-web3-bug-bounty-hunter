---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Allow custom Creator and Collector names to be emitted in `IStory` events to
  build artwork provenance
vuln_class: []
---

# Allow custom Creator and Collector names to be emitted in `IStory` events to build artwork provenance

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** The `IStory` interface is designed to allow custom names to be emitted for the Creator and Collector events. Here is an [example](https://www.transient.xyz/nfts/base/0x6c81306129b3cc63b0a6c7cec3dd50721ac378fe/9) where a Creator has used the custom name `lytke`.

But in CryptoArt's implementation of `IStory` interface, custom names are not allowed and it is always the caller's hex string that will be set:
```solidity
function addCollectionStory(string calldata, /*creatorName*/ string calldata story) external onlyOwner {
    emit CollectionStory(msg.sender, msg.sender.toHexString(), story);
}

/// @inheritdoc IStory
function addCreatorStory(uint256 tokenId, string calldata, /*creatorName*/ string calldata story)
    external
    onlyTokenOwner(tokenId)
{
    emit CreatorStory(tokenId, msg.sender, msg.sender.toHexString(), story);
}

/// @inheritdoc IStory
function addStory(uint256 tokenId, string calldata, /*collectorName*/ string calldata story)
    external
    onlyTokenOwner(tokenId)
{
    emit Story(tokenId, msg.sender, msg.sender.toHexString(), story);
}
```

**Impact:** Custom names should be allowed as they form part of the "provenance" of an artwork; the value of an artwork is often based on who the creator was and if it has been held by significant collectors in the past. Proper custom names are a lot easier to remember and tell a story about rather than 0x1343335...Artworks with custom names will be able to build a better story around them resulting in improved "provenance".

**CryptoArt:**
Fixed in commit [77f34a4](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/77f34a49cbc27589f3179b35b58a86696696bf83).

**Cyfrin:** Verified.
