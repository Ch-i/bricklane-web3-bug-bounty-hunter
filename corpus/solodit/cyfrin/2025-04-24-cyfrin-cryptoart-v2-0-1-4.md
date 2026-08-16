---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-1-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: '`IERC7160` specification requires `pinTokenURI` to revert for non-existent
  `tokenId`'
vuln_class: []
---

# `IERC7160` specification requires `pinTokenURI` to revert for non-existent `tokenId`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** Per the specification of `IERC7160`:
```solidity
/// @notice Pin a specific token uri for a particular token
/// @dev This call MUST revert if the token does not exist
function pinTokenURI(uint256 tokenId, uint256 index) external;
```

But the implementation of `pinTokenURI` doesn't revert for tokens which don't exist, since `_tokenURIs[tokenId].length` will always equal 2 even for non-existent `tokenId`:
```solidity
// mapping value always has fixed array size of 2
mapping(uint256 tokenId => string[2] tokenURIs) private _tokenURIs;

function pinTokenURI(uint256 tokenId, uint256 index) external onlyOwner {
    if (index >= _tokenURIs[tokenId].length) {
        revert Error.Token_IndexOutOfBounds(tokenId, index, _tokenURIs[tokenId].length - 1);
    }

    _pinnedURIIndex[tokenId] = index;

    emit TokenUriPinned(tokenId, index);
    emit MetadataUpdate(tokenId);
}
```

**Recommended Mitigation:** Use the `onlyIfTokenExists` modifier:
```diff
-    function pinTokenURI(uint256 tokenId, uint256 index) external onlyOwner {
+    function pinTokenURI(uint256 tokenId, uint256 index) external onlyIfTokenExists(tokenId) onlyOwner {
```

**CryptoArt:**
Fixed in commit [0409ae4](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/0409ae4d81225a351c4d42620502843242f2604f).

**Cyfrin:** Verified.
