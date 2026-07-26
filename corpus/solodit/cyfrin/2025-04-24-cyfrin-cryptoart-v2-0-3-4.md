---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-3-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: '`burn` should delete `tokenURI` related data and emit `TokenUriUnpinned` event'
vuln_class: []
---

# `burn` should delete `tokenURI` related data and emit `TokenUriUnpinned` event

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** The `burn` function should delete `tokenURI` related data and emit `TokenUriUnpinned` event:
```diff
    function burn(uint256 tokenId) public override whenNotPaused {
        // require sender is owner or approved has been removed as the internal burn function already checks this
        ERC2981Upgradeable._resetTokenRoyalty(tokenId);
        ERC721BurnableUpgradeable.burn(tokenId);
        emit Burned(tokenId);
+       emit TokenUriUnpinned(tokenId);
+       delete _tokenURIs[tokenId];
+       delete _pinnedURIIndex[tokenId];
+       delete _hasPinnedTokenURI[tokenId];
    }
```

This provides a gas refund as part of the burn and also removes token data that should no longer exist. It also prevents `hasPinnedTokenURI` from returning `true` for a burned token since that function doesn't check for valid token id (another issue has been created to track this).

**CryptoArt:**
Fixed in commit [b554763](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/b5547630515c8da112db6754a3e25dda1e69b4a7).

**Cyfrin:** Verified.
