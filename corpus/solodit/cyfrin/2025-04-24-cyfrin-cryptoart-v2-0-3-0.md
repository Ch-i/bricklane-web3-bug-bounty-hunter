---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-3-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Prefer named return parameters, especially for `memory` returns
vuln_class: []
---

# Prefer named return parameters, especially for `memory` returns

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** Prefer named return parameters, especially for memory returns. For example `tokenURIs` can be refactored to remove local variables and explicit return:
```solidity
function tokenURIs(uint256 tokenId)
    external
    view
    override
    onlyIfTokenExists(tokenId)
    returns (uint256 index, string[2] memory uris, bool isPinned)
{
    index = _getTokenURIIndex(tokenId);
    uris = _tokenURIs[tokenId];
    isPinned = _hasPinnedTokenURI[tokenId];
}
```

**CryptoArt:**
Fixed in commit [bdd28fa](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/bdd28fa71f8d445fb3306a1fdc16b49fa5b5d1e4).

**Cyfrin:** Verified.
