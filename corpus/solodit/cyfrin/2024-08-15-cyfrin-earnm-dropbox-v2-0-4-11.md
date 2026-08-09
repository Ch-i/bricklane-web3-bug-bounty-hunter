---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-11
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Bypass first `for` loop in `DropBoxFractalProtocol::_determineTier` when `randomNumber
  >= TIER_1_MAX_BOXES`
vuln_class: []
---

# Bypass first `for` loop in `DropBoxFractalProtocol::_determineTier` when `randomNumber >= TIER_1_MAX_BOXES`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Tier 1 is the lowest tier with the most boxes and this condition inside the first `for` loop ensures the first `for` loop will always fails to allocate a `tierId` when `randomNumber >= TIER_1_MAX_BOXES`:
```solidity
// Check if the randomNumber falls within the current tier's range and hasn't exceeded the mint limit.
if ((randomNumber < maxBoxesPerTier) && hasCapacity) return tierId;
```

Hence there is no point entering the first `for` loop when `randomNumber >= TIER_1_MAX_BOXES`; skip the first `for` loop and go straight to the second one:
```diff
  function _determineTier(
    uint256 randomNumber,
    uint256[TIER_IDS_ARRAY_LEN] memory mintedTierAmountCache
  )
    internal
    view
    returns (uint128 /* tierId, function returns before the end of the execution */ )
  {
-    // Iterate backwards from the highest tier to the lowest.
-    for (uint128 tierId = TIER_IDS_LENGTH; tierId > 0; tierId--) {

+    // impossible for first loop to allocate tierId when randomNumber is
+    // >= lowest tier max boxes, so in that case skip to second loop
+    if(randomNumber < TIER_1_MAX_BOXES) {
+      // Iterate backwards from the highest tier to the lowest.
+      for (uint128 tierId = TIER_IDS_LENGTH; tierId > 0; tierId--) {
```

**Mode:**
Fixed in commit [a3d7641](https://github.com/Earnft/dropbox-smart-contracts/commit/a3d7641b472130cadc8502426ee49dbbc4d947d2).

**Cyfrin:** Verified.
