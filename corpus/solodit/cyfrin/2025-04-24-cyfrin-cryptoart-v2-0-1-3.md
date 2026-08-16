---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-1-3
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
title: '`IERC7160` specification requires `hasPinnedTokenURI` to revert for non-existent
  `tokenId`'
vuln_class: []
---

# `IERC7160` specification requires `hasPinnedTokenURI` to revert for non-existent `tokenId`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** Per the specification of `IERC7160`:
```solidity
/// @notice Check on-chain if a token id has a pinned uri or not
/// @dev This call MUST revert if the token does not exist
function hasPinnedTokenURI(uint256 tokenId) external view returns (bool pinned);
```

But the implementation of `hasPinnedTokenURI` doesn't revert for tokens which don't exist, instead it will simply return `false` or even return `true` if a token was burned when the value was true since burning doesn't delete `_hasPinnedTokenURI` (another issue has been created to track this):
```solidity
function hasPinnedTokenURI(uint256 tokenId) external view returns (bool) {
    return _hasPinnedTokenURI[tokenId];
}
```

**Recommended Mitigation:** Use the `onlyIfTokenExists` modifier:
```diff
-    function hasPinnedTokenURI(uint256 tokenId) external view returns (bool) {
+    function hasPinnedTokenURI(uint256 tokenId) external view onlyIfTokenExists(tokenId) returns (bool) {
```

**CryptoArt:**
Fixed in commit [56d0e22](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/56d0e222cdf25a971cd6466fd4757185a4362069).

**Cyfrin:** Verified.
