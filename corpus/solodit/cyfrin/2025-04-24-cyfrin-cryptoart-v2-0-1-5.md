---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-1-5
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
title: Inconsistent pause functionality allows certain state-changing operations when
  contract is paused
vuln_class: []
---

# Inconsistent pause functionality allows certain state-changing operations when contract is paused

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** The `CryptoartNFT` contract implements a pause mechanism using OpenZeppelin's `PausableUpgradeable` contract. However, the pause functionality is inconsistently applied across the contract's functions. While minting and burning operations are properly protected with the `whenNotPaused` modifier, several other state-changing functions remain accessible even when the contract is paused, including token transfers, metadata management, and story-related functions.

The following state-changing functions lack the `whenNotPaused` modifier:

1. Token transfers and approvals (inherited from ERC721)
2. Metadata management functions:
   - `updateMetadata`
   - `pinTokenURI`
   - `markAsRedeemable`
3. Story-related functions:
   - `addCollectionStory`
   - `addCreatorStory`
   - `addStory`
   - `toggleStoryVisibility`

**Impact:** When the contract is paused (typically during emergencies or upgrades), users can still perform various state-changing operations that might be undesirable during a pause period. It could lead to unexpected state changes during contract upgrades or emergency situations.

**Recommended Mitigation:** Add the `whenNotPaused` modifier to all state-changing functions to ensure consistent behavior when the contract is paused. For example:

**Cryptoart:**
Fixed in commit [e7d7e5b](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/e7d7e5b3b1c8976a11d49f889b4168ce649be2ee).

**Cyfrin:** Verified.

\clearpage
