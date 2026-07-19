---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Use named constants to indicate purpose of magic numbers
vuln_class: []
---

# Use named constants to indicate purpose of magic numbers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** Use named constants to indicate purpose of magic numbers. For example in reference to the value of the `_tokenURIs` mapping:
* instead of using literal `2`, use existing named constant `URIS_PER_TOKEN`:
```solidity
CryptoartNFT.sol
72:    mapping(uint256 tokenId => string[2] tokenURIs) private _tokenURIs;
358:        returns (uint256, string[2] memory, bool)
361:        string[2] memory uris = _tokenURIs[tokenId];
698:        string[2] memory uris = _tokenURIs[tokenId];
```

* when setting uris in `updateMetadata` and `_setTokenURIs`, use named constants for the indexes:
```solidity
function updateMetadata(uint256 tokenId, string calldata newRedeemableURI, string calldata newNotRedeemableURI)
    external
    onlyOwner
    onlyIfTokenExists(tokenId)
{
    _tokenURIs[tokenId][URI_REDEEMABLE_INDEX] = newRedeemableURI;
    _tokenURIs[tokenId][URI_NOT_REDEEMABLE_INDEX] = newNotRedeemableURI;
    emit MetadataUpdate(tokenId); // ERC4906
}
```

This can also save gas for example in `pinTokenURI`, instead of using `_tokenURIs[tokenId].length` just use the constant `URIS_PER_TOKEN` since it never changes:
```solidity
function pinTokenURI(uint256 tokenId, uint256 index) external onlyOwner {
    if (index >= URIS_PER_TOKEN) {
        revert Error.Token_IndexOutOfBounds(tokenId, index, URIS_PER_TOKEN - 1);
    }
```

**CryptoArt:**
Fixed in commit [97ef0ad](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/97ef0add6848540e158927092d0a1af820e840fe).

**Cyfrin:** Verified.
