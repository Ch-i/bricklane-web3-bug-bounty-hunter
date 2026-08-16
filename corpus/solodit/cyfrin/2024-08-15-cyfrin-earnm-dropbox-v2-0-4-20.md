---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-20
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Only read and write storage location `unclaimedTierAmount` once per changed
  tier in `DropBox::_assignTierAndMint`
vuln_class: []
---

# Only read and write storage location `unclaimedTierAmount` once per changed tier in `DropBox::_assignTierAndMint`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `DropBox::_assignTierAndMint` can be re-written to drastically reduce the amount of storage read/writes to `unclaimedTierAmount` storage location like this:
```solidity
  function _assignTierAndMint(
    uint32 boxAmount,
    uint256[] memory randomNumbers,
    address claimer,
    bytes memory code
  )
    internal
  {
    uint256[] memory boxIdsToEmit = new uint256[](boxAmount);

    // [Gas] Cache mintedTierAmount and update cache during the loop to prevent
    // _determineTier() from re-reading it from storage multiple times and
    // to prevent multiple update storage writes
    uint256[TIER_IDS_ARRAY_LEN] memory mintedTierAmountCache = mintedTierAmount;

    // [Gas] Cache unclaimedTierAmount and update cache during the loop then
    // write to storage at the end to prevent multiple update storage writes
    uint256[TIER_IDS_ARRAY_LEN] memory unclaimedTierAmountCache;

    // [Gas] Cache the tier changed indicator to update storage only for tiers which changed
    bool[TIER_IDS_ARRAY_LEN] memory tierChangedInd;

    // [Gas] cache the current boxId, use cache during the loop then write once
    // at the end; this results in only 1 storage read and 1 storage write for `boxIdCounter`
    uint256 boxIdCounterCache = boxIdCounter;

    // For each box to mint
    for (uint32 i; i < boxAmount; i++) {
      // [Memory] Add the box id to the boxes ids array
      boxIdsToEmit[i] = boxIdCounterCache++;

      // The box seed is directly derived from the random number without any
      // additional values like the box id, the claimer address, or the block timestamp.
      // This is made like this to ensure the tier assignation of the box is purely random
      // and the tier that the box is assigned to, won't change after the randomness is fulfilled.
      // The only way to predict the seed is to know the random number.
      // Random number validation is done in the _fulfillRandomWords function.
      uint256 boxSeed = uint256(keccak256(abi.encode(randomNumbers[i])));

      // Generate a random number between 0 and TOTAL_MAX_BOXES - 1 using the pure random seed
      // Modulo ensures that the random number is within the range of [0, TOTAL_MAX_BOXES) (upper bound exclusive),
      // providing a uniform distribution across the possible range. This ensures that each tier has a
      // probability of being selected proportional to its maximum box count. The randomness is normalized
      // to fit within the predefined total boxes, maintaining the intended probability distribution for each tier.
      //
      // Example with the following setup:
      // _tierMaxBoxes -> [1, 10, 100, 1000, 2000, 6889]
      // _tierNames -> ["Mythical Box", "Legendary Box", "Epic Box", "Rare Box", "Uncommon Box", "Common Box"]
      //
      // The `TOTAL_MAX_BOXES` is the sum of `_tierMaxBoxes`, which is 10_000.
      // The probability distribution is as follows:
      //
      // Mythical Box:   1    / 10_000  chance.
      // Legendary Box:  10   / 10_000  chance.
      // Epic Box:       100  / 10_000  chance.
      // Rare Box:       1000 / 10_000  chance.
      // Uncommon Box:   2000 / 10_000  chance.
      // Common Box:     6889 / 10_000  chance.
      //
      // By using the modulo operation with TOTAL_MAX_BOXES, the random number's probability
      // to land in any given tier is determined by the number of max boxes available for that tier
      uint256 randomNumber = boxSeed % TOTAL_MAX_BOXES;

      // Determine the tier of the box based on the random number
      uint128 tierId = _determineTier(randomNumber, mintedTierAmountCache);

      // if the tier amount cache hasn't been updated for this tier type
      if(!tierChangedInd[tierId]) {
          // then set it as updated
          tierChangedInd[tierId] = true;

          // cache the current amounts once from storage
          unclaimedTierAmountCache[tierId] = unclaimedTierAmount[tierId];
      }

      // [Gas] Adjust the cached amounts for this tier
      ++mintedTierAmountCache[tierId];
      ++unclaimedTierAmountCache[tierId];

      // Save the box to the boxIdToBox mapping
      boxIdToBox[boxIdsToEmit[i]] = Box({ blockTs: uint128(block.timestamp), tier: tierId });

      // Mint NFT for this box; explicitly not using `_safeMint` to prevent re-entrancy issues
      _mint(claimer, boxIdsToEmit[i]);
    }

    // Update storage for boxIdCounter
    boxIdCounter = boxIdCounterCache;

    // Update tier storage only for tiers which were changed
    for (uint128 tierId = 1; tierId < TIER_IDS_ARRAY_LEN; tierId++) {
      if (tierChangedInd[tierId]) {
        mintedTierAmount[tierId] = mintedTierAmountCache[tierId];
        unclaimedTierAmount[tierId] = unclaimedTierAmountCache[tierId];
      }
    }

    // Emit an event indicating the boxes have been minted
    emit BoxesMinted(claimer, boxIdsToEmit, code);
  }
```

When we made this change we noticed that `test_assignTierAndMint_InvalidBoxAmount` started to fail but this test doesn't seem to be valid since the `boxAmount` input is validated prior to `_assignTierAndMint` being called, hence we believe this test should be deleted as it is not relevant to the current codebase.

**Mode:**
Fixed in commit [79eea07](https://github.com/Earnft/dropbox-smart-contracts/commit/79eea078baf6bf855e5a5854981ac60c88f46118).

**Cyfrin:** Verified.
