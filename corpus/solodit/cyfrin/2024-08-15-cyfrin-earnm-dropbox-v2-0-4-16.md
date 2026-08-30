---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-16
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Only read and write once for storage locations `boxIdCounter` and `mintedTierAmount`
  in `DropBox::_assignTierAndMint`
vuln_class: []
---

# Only read and write once for storage locations `boxIdCounter` and `mintedTierAmount` in `DropBox::_assignTierAndMint`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** In `DropBox::_assignTierAndMint`, `boxIdCounter` and `mintedTierAmount` can be cached before the loop, use the cached version during the loop and finally update once at the end:
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

    // [Gas] Cache mintedTierAmount, update cache during the loop and record
    // which tiers were updated. At the end of the loop write once to storage
    // only for tiers which were updated. Also prevents `_determineTier` from
    // re-reading storage multiple times
    bool[TIER_IDS_ARRAY_LEN] memory tierChangedInd;
    uint256[TIER_IDS_ARRAY_LEN] memory mintedTierAmountCache = mintedTierAmount;

    // [Gas] cache the current boxId, use cache during the loop then write once
    // at the end; this results in only 1 storage read and 1 storage write for `boxIdCounter`
    uint256 boxIdCounterCache = boxIdCounter;

    // For each box to mint
    for (uint32 i; i < boxAmount; i++) {
      // Generate a new box id, starting from 1
      uint256 newBoxId = boxIdCounterCache++;

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

      // Increment the cached amount for this tier and mark this tier as changed
      ++mintedTierAmountCache[tierId];
      tierChangedInd[tierId] = true;

      // [Memory] Add the box id to the boxes ids array
      boxIdsToEmit[i] = newBoxId;

      // Save the box to the boxes mappings
      _saveBox(newBoxId, tierId);

      // Mint the box; explicitly not using `_safeMint` to prevent
      // re-entrancy issues
      _mint(claimer, newBoxId);
    }

    // update storage for boxIdCounter
    boxIdCounter = boxIdCounterCache;

    // update storage for mintedTierAmount only for tiers which were changed
    // hence each tier from mintedTierAmount storage is read only once and only
    // tiers which changed are written to storage only once
    for(uint128 tierId = 1; tierId<TIER_IDS_ARRAY_LEN; tierId++) {
      if(tierChangedInd[tierId]) {
        mintedTierAmount[tierId] = mintedTierAmountCache[tierId];
      }
    }

    // Emit an event indicating the boxes have been minted
    emit BoxesMinted(claimer, boxIdsToEmit, code);
  }
```

The supplied code also has a couple of other useful changes inside the loop:
* `mintedTierAmountCache` and `boxIdsToEmit` are changed before calling `_saveBox` and `_mint` (Effects before Interactions)
* comment added to note that `_mint` is being explicitly used instead of `_safeMint`

We also found that the unit testing around `mintedTierAmount` was lacking in that we could comment out lines of code and all the tests would still pass, so we added more unit tests around this area:

File: `test/mocks/DropBoxMock.sol`
```solidity
// couple of helper functions
  /// @dev [Test purposes] Test get the minted tier amounts
  function mock_getMintedTierAmount(uint128 tierId) public view returns (uint256) {
    return mintedTierAmount[tierId];
  }
  function mock_getMintedTierAmounts() public view returns (uint256[TIER_IDS_ARRAY_LEN] memory) {
    return mintedTierAmount;
  }
```

File: `test/DropBox/behaviors/revealDropBox/revealDropBoxes.t.sol`
```solidity
// firstly over-write the `_validateMinting` function to perform additional verification
  function _validateMinting(
    uint256[TIER_IDS_ARRAY_LEN] memory prevMintedTierAmounts,
    uint32 boxAmount,
    string memory code) internal
  {
    uint256[] memory expectedBoxIds = new uint256[](boxAmount);
    for (uint256 i; i < boxAmount; i++) {
      expectedBoxIds[i] = i + 1;
    }

    vm.expectEmit(address(dropBox));
    emit DropBoxFractalProtocolLib.BoxesMinted(users.stranger, expectedBoxIds, abi.encode(code));
    _fundAndReveal(users.stranger, code, 1 ether);

    (uint256 blockTs, uint256 tier, address owner) = dropBox.getBox(1);
    assertEq(owner, users.stranger);
    assertGt(tier, 0);
    assertLt(tier, 7);

    // iterate over the boxes to get their types and update the
    // previous minted tier amounts
    for (uint256 i; i < expectedBoxIds.length; i++) {
      (,uint128 boxTierId, address owner) = dropBox.getBox(expectedBoxIds[i]);
      assertEq(owner, users.stranger);

      // increment previously minted tierId for this tier
      ++prevMintedTierAmounts[boxTierId];
    }

    // verify DropBox::mintedTierAmount has been correctly changed
    for(uint128 tierId = 1; tierId < TIER_IDS_ARRAY_LEN; tierId++) {
      assertEq(dropBox.mock_getMintedTierAmount(tierId), prevMintedTierAmounts[tierId]);
    }
  }

// next in the tests where _validateMinting is called, simply replace the call with this line
_validateMinting(dropBox.mock_getMintedTierAmounts(), boxAmount, code);
```

**Mode:**
Fixed in commit [5badac3](https://github.com/Earnft/dropbox-smart-contracts/commit/5badac3a5a6de31d0ad84decdefd0e4938e07be3).

**Cyfrin:** Verified.
