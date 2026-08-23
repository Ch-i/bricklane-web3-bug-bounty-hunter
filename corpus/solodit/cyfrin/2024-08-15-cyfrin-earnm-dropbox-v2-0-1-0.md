---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: '`DropBox::tokenURI` returns data for non-existent `tokenId` violating `EIP721`'
vuln_class: []
---

# `DropBox::tokenURI` returns data for non-existent `tokenId` violating `EIP721`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `DropBox::tokenURI` overrides OpenZeppelin's default implementation with the following code:
```solidity
function tokenURI(uint256 tokenId) public view override returns (string memory) {
  return string(abi.encodePacked(bytes(_baseTokenURI), Strings.toString(tokenId), ".json"));
}
```

This implementation does not check that `tokenId` exists and hence will return data for non-existent `tokenId`. This is in contrast to OpenZeppelin's [implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L88-L93) and contrary to [EIP721](https://eips.ethereum.org/EIPS/eip-721) which states:

```solidity
/// @notice A distinct Uniform Resource Identifier (URI) for a given asset.
/// @dev Throws if `_tokenId` is not a valid NFT. URIs are defined in RFC
///  3986. The URI may point to a JSON file that conforms to the "ERC721
///  Metadata JSON Schema".
function tokenURI(uint256 _tokenId) external view returns (string);
```

**Impact:** Apart from simply returning incorrect data, the most likely negative effect is integration problems with NFT marketplaces.

**Recommended Mitigation:** Revert if `tokenId` does not exist:
```diff
function tokenURI(uint256 tokenId) public view override returns (string memory) {
+ _requireOwned(tokenId);
  return string(abi.encodePacked(bytes(_baseTokenURI), Strings.toString(tokenId), ".json"));
}
```

**Mode:**
Fixed in commit [2d8c3c0](https://github.com/Earnft/dropbox-smart-contracts/commit/2d8c3c0142f70fae183f1185ea1987a0707711ef).

**Cyfrin:** Verified.
