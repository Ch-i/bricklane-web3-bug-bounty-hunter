---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Resolve discrepancy between expected `randomNumber` in `DropBox::_assignTierAndMint`
  and `DropBoxFractalProtocol::_determineTier`
vuln_class: []
---

# Resolve discrepancy between expected `randomNumber` in `DropBox::_assignTierAndMint` and `DropBoxFractalProtocol::_determineTier`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `DropBox::_assignTierAndMint`  generates `randomNumber` between 0 and 9999 and then calls `DropBoxFractalProtocol::_determineTier` passing this as input:
```solidity
// Generate a random number between 0 and 9999
uint256 randomNumber = boxSeed % 10_000;

// Determine the tier of the box based on the random number
uint128 tierId = _determineTier(randomNumber, mintedTierAmountCache);
```

But `DropBoxFractalProtocol::_determineTier`  has a comment expecting `randomNumber` to be between 0 and 999_999:
```solidity
/// @notice Function to determine the tier of the box based on the random number.
/// @param randomNumber The random number to use to determine the tier. 0 to 999_999
/// @param mintedTierAmountCache Total cached amount minted for each tier.
/// @return determinedTierId The tier id of the box.
function _determineTier(uint256 randomNumber, ...)
```

Resolve this discrepancy; it appears that the comment in the latter is incorrect.

**Mode:**
Fixed in commit [4e48b15](https://github.com/Earnft/dropbox-smart-contracts/commit/4e48b15237e0e9f21fa5666595a05fb645d722c6) & [5a3cbf9](https://github.com/Earnft/dropbox-smart-contracts/commit/5a3cbf9b68d1f426bce08984b06b1c92d7675385).

**Cyfrin:** Verified.
