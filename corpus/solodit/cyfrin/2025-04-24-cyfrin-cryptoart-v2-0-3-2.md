---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Remove obsolete `onlyTokenOwner` from `_transferToNftReceiver`
vuln_class: []
---

# Remove obsolete `onlyTokenOwner` from `_transferToNftReceiver`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** Since `_transferToNftReceiver` calls `ERC721Upgradeable::safeTransferFrom`, the `onlyTokenOwner` modifier is obsolete and inefficient as:
* `safeTransferFrom` [calls](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/release-v5.1/contracts/token/ERC721/ERC721Upgradeable.sol#L183) `transferFrom`
* `transferFrom` [calls](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/release-v5.1/contracts/token/ERC721/ERC721Upgradeable.sol#L166) `_update` passing `_msgSender()` as the last `auth` parameter
* `_update` [calls](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/release-v5.1/contracts/token/ERC721/ERC721Upgradeable.sol#L274) `_checkAuthorized` since the `auth` parameter was valid
* `_checkAuthorized` [calls](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/release-v5.1/contracts/token/ERC721/ERC721Upgradeable.sol#L215-L238) `_isAuthorized` which verifies the caller is either the token's owner or someone who the token owner has approved

**CryptoArt:**
Fixed in commit [75e179b](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/75e179b3cea8855977a391ace169313053bc2de5).

**Cyfrin:** Verified.
