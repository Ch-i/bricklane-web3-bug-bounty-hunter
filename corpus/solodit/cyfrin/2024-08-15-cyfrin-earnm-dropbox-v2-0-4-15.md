---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-15
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use a simplified and more efficient implementation for `DropBoxFractalProtocol::_determineTier`
vuln_class: []
---

# Use a simplified and more efficient implementation for `DropBoxFractalProtocol::_determineTier`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Use a simplified and more efficient implementation for `DropBoxFractalProtocol::_determineTier` such as:
```solidity
  function _determineTier(
    uint256 randomNumber,
    uint256[TIER_IDS_ARRAY_LEN] memory mintedTierAmountCache
  )
    internal
    view
    returns (uint128 /* tierId, function returns before the end of the execution */ )
  {
    // if the randomNumber is smaller than TIER_1_MAX_BOXES, first attempt
    // tier selection which prioritizes the most valuable tiers for selection where:
    // 1) randomNumber falls within one or more tiers AND
    // 2) the tier(s) have not been exhausted
    if(randomNumber < TIER_1_MAX_BOXES) {
      if(randomNumber < TIER_6_MAX_BOXES && mintedTierAmountCache[6] < TIER_6_MAX_BOXES) return 6;
      if(randomNumber < TIER_5_MAX_BOXES && mintedTierAmountCache[5] < TIER_5_MAX_BOXES) return 5;
      if(randomNumber < TIER_4_MAX_BOXES && mintedTierAmountCache[4] < TIER_4_MAX_BOXES) return 4;
      if(randomNumber < TIER_3_MAX_BOXES && mintedTierAmountCache[3] < TIER_3_MAX_BOXES) return 3;
      if(randomNumber < TIER_2_MAX_BOXES && mintedTierAmountCache[2] < TIER_2_MAX_BOXES) return 2;
      if(randomNumber < TIER_1_MAX_BOXES && mintedTierAmountCache[1] < TIER_1_MAX_BOXES) return 1;
    }

    // if we get here it means that either:
    // 1) randomNumber >= TIER_1_MAX_BOXES OR
    // 2) the tier(s) randomNumber fell into had been exhausted
    //
    // in this case we attempt to allocate based on what is available
    // prioritizing from the least valuable tiers
    if(mintedTierAmountCache[1] < TIER_1_MAX_BOXES) return 1;
    if(mintedTierAmountCache[2] < TIER_2_MAX_BOXES) return 2;
    if(mintedTierAmountCache[3] < TIER_3_MAX_BOXES) return 3;
    if(mintedTierAmountCache[4] < TIER_4_MAX_BOXES) return 4;
    if(mintedTierAmountCache[5] < TIER_5_MAX_BOXES) return 5;
    if(mintedTierAmountCache[6] < TIER_6_MAX_BOXES) return 6;

    // if we get here it means that all tiers have been exhausted
    revert NoMoreBoxesToMint();
  }
```

**Mode:**
Fixed in commit [0e3410b](https://github.com/Earnft/dropbox-smart-contracts/commit/0e3410b6bdf8150e3ed613af2713747cd93084f8).

**Cyfrin:** Verified.
