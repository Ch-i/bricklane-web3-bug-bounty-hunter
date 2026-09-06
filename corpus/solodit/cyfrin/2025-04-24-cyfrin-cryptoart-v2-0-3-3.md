---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: In `tokenURI` avoid copying entire `_tokenURIs[tokenId]` from `storage` into
  `memory`
vuln_class: []
---

# In `tokenURI` avoid copying entire `_tokenURIs[tokenId]` from `storage` into `memory`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** `tokenURI` only uses the "pinned" URI index so there's no reason to copy both token URIs from `storage` to `memory`. Simply use a `storage` reference like this:
```diff
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721Upgradeable)
        onlyIfTokenExists(tokenId)
        returns (string memory)
    {
-       string[2] memory uris = _tokenURIs[tokenId];
+       string[2] storage uris = _tokenURIs[tokenId];
        string memory uri = uris[_getTokenURIIndex(tokenId)];

        if (bytes(uri).length == 0) {
            revert Error.Token_NoURIFound(tokenId);
        }

        return string.concat(_baseURI(), uri);
    }
```

**CryptoArt:**
Fixed in commit [591fed0](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/591fed0798ab0cd61fe965c9a4d0b3e8461e0f12).

**Cyfrin:** Verified.
