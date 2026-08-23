---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-19
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
title: Only read and write storage location `unclaimedTierAmount` once per changed
  tier in `DropBox::claimDropBoxes`
vuln_class: []
---

# Only read and write storage location `unclaimedTierAmount` once per changed tier in `DropBox::claimDropBoxes`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `DropBox::claimDropBoxes` can be re-written to drastically reduce the amount of storage read/writes to `unclaimedTierAmount` storage location like this:
```solidity
  function claimDropBoxes(uint256[] calldata _boxIds) external payable nonReentrant {
    //
    //
    //
    //  Request Checks
    // ---------------------------------------------------------------------------------------------
    // [Safety check] Only allowed to claim if the isEarnmClaimAllowed variable is true
    // Can be modified by the owner as a safety measure
    if (!(isEarnmClaimAllowed)) revert Unauthorized();

    // [Safety check] Validate that the boxIds array is not empty
    if (_boxIds.length == 0) revert Unauthorized();

    // Require that the user sends a fee of "claimFee" amount
    if (msg.value != claimFee) revert InvalidClaimFee();
    // ---------------------------------------------------------------------------------------------

    // Amount of Earnm tokens to claim
    uint256 amountToClaim;

    // [Gas] Cache unclaimedTierAmount and update cache during the loop then
    // write to storage at the end to prevent multiple update storage writes
    uint256[TIER_IDS_ARRAY_LEN] memory unclaimedTierAmountCache;

    // [Gas] Cache the tier changed indicator to update storage only for tiers which changed
    bool[TIER_IDS_ARRAY_LEN] memory tierChangedInd;

    //
    //
    //
    //  Earnm Calculation and Safety Checks
    // ---------------------------------------------------------------------------------------------
    // Iterate over box IDs to calculate rewards and validate ownership and uniqueness.
    // - Validate that the sender is the owner of the boxes
    // - Validate that the sender has enough boxes to claim
    // - Validate that the box ids are valid
    // - Validate that the box ids are not duplicated
    // - Calculate the amount of Earnm tokens to claim given the box ids
    for (uint256 i; i < _boxIds.length; i++) {
      // [Safety check] Duplicate values are not allowed
      if (i > 0 && _boxIds[i - 1] >= _boxIds[i]) revert BadRequest();

      // [Safety check] Validate that the box owner is the sender
      if (ownerOf(_boxIds[i]) != msg.sender) revert Unauthorized();

      // Copy the box from the boxes mappings
      Box memory box = boxIdToBox[_boxIds[i]];

      // Increment the amount of Earnm tokens to send to the sender
      amountToClaim += _calculateVestingPeriodPerBox(box.tier, box.blockTs, TIER_IDS_LENGTH);

      // if the unclaimed cache hasn't been updated for this tier type
      if(!tierChangedInd[box.tier]) {
          // then set it as updated
          tierChangedInd[box.tier] = true;

          // cache the current amount once from storage
          unclaimedTierAmountCache[box.tier] = unclaimedTierAmount[box.tier];
      }

      // decrement the unclaimed cached amount for this tier
      --unclaimedTierAmountCache[box.tier];

      // Delete the box from the boxIdToBox mapping
      delete boxIdToBox[_boxIds[i]];

      // Burn the ERC721 token corresponding to the deleted box
      _burn(_boxIds[i]);
    }

    // [Safety check] In case the amount to claim is 0, revert
    if (amountToClaim == 0) revert AmountOfEarnmToClaimIsZero();

    // Update tier storage only for tiers which were changed
    for (uint128 tierId = 1; tierId < TIER_IDS_ARRAY_LEN; tierId++) {
      if (tierChangedInd[tierId]) unclaimedTierAmount[tierId] = unclaimedTierAmountCache[tierId];
    }

    // ---------------------------------------------------------------------------------------------

    //
    //
    //
    //  Contract Earnm Balance and Safety Checks
    // ---------------------------------------------------------------------------------------------
    // Get the balance of Earnm ERC20 tokens of the contract
    uint256 balance = EARNM.balanceOf(address(this));

    // [Safety check] Validate that the contract has enough Earnm tokens to cover the claim
    if (balance < amountToClaim) revert InsufficientEarnmBalance();
    // ---------------------------------------------------------------------------------------------

    // Emit an event indicating the boxes have been claimed
    emit BoxesClaimed(msg.sender, _boxIds, amountToClaim);

    // Transfer the tokens to the sender
    EARNM.safeTransfer(msg.sender, amountToClaim);
    // ---------------------------------------------------------------------------------------------

    //
    //
    //
    //  Claim Fee Transfer
    // ---------------------------------------------------------------------------------------------
    _sendFee(msg.value);
    // ---------------------------------------------------------------------------------------------
  }
```

With this version the `DropBox::_deleteBox` function is no longer required and should be deleted along with its associated test file and helper function in `DropBoxMock.sol`.

We also noticed through mutation testing that updates to storage for `unclaimedTierAmount` and `boxIdToBox` which occur during the claim process were not being verified by the existing test suite, so added new features to the test suite to cover this:

File: `test/mocks/DropBoxMock.sol`
```solidity
// new helper function
  /// @dev [Test purposes] Test get all the unclaimed tier amounts
  function mock_getUnclaimedTierAmounts() public view returns (uint256[TIER_IDS_ARRAY_LEN] memory) {
    return unclaimedTierAmount;
  }
```

File: `test/DropBox/behaviors/claimDropBox/claimDropBox.t.sol`
```solidity
// updated this helper function to return the expected unclaimed amounts
  function _calculateExpectedClaimAmount(uint256[] memory boxIds) internal view
  returns (uint256 totalClaimAmount, uint256[TIER_IDS_ARRAY_LEN] memory expectedUnclaimedTierAmounts) {
    // first load the existing unclaimed tier amounts
    expectedUnclaimedTierAmounts = dropBox.mock_getUnclaimedTierAmounts();

    // iterate through the boxes that will be claimed
    for (uint256 i; i < boxIds.length; i++) {
      // get timestamp & tier
      (uint128 blockTs, uint128 tier,) = dropBox.getBox(boxIds[i]);

      // calculate expected token claim amount
      totalClaimAmount += dropBox.mock_calculateVestingPeriodPerBox(tier, blockTs, TIER_IDS_LENGTH);

      // update expected unclaimed tier amount
      --expectedUnclaimedTierAmounts[tier];
    }
  }

// updated this helper function to validate the expected amounts
  function _validateClaimedBoxes(
    uint256[TIER_IDS_ARRAY_LEN] memory expectedUnclaimedTierAmounts,
    uint256[] memory boxIds,
    uint256 expectedAmount,
    address claimer) internal
  {
    for (uint256 i; i < boxIds.length; i++) {
      // get info for deleted box
      (uint128 blockTs, uint128 tier, address owner) = dropBox.getBox(boxIds[i]);

      // box should no longer be owned
      assertEq(owner, address(0));

      // box should be deleted from boxIdToBox mapping
      assertEq(blockTs, 0);
      assertEq(tier, 0);
    }

    // verify DropBox::unclaimedTierAmount has been correctly decreased
    for(uint128 tierId = 1; tierId < TIER_IDS_ARRAY_LEN; tierId++) {
      assertEq(dropBox.mock_getUnclaimedTierAmount(tierId), expectedUnclaimedTierAmounts[tierId]);
    }

    // verify expected earnm contract balance after claims processed
    uint256 earnmBalance = earnmERC20Token.balanceOf(claimer);
    assertEq(earnmBalance, expectedAmount);

    emit DropBoxFractalProtocolLib.BoxesClaimed(claimer, boxIds, expectedAmount);
  }

// updated 2 test functions to use the new updated helper functions
  function test_claimDropBoxes_valid() public {
    string memory code = "validCode";
    address allowedAddress = users.stranger;
    uint32 boxAmount = 5;
    uint256[] memory boxIds = new uint256[](boxAmount);
    uint256 earnmAmount = 1000 * 1e18;

    _setupClaimEnvironment(code, allowedAddress, boxAmount, boxIds, earnmAmount);

    (uint256 expectedAmount, uint256[TIER_IDS_ARRAY_LEN] memory expectedUnclaimedTierAmounts)
      = _calculateExpectedClaimAmount(boxIds);

    _fundAndClaim(allowedAddress, boxIds, 1 ether);
    _validateClaimedBoxes(expectedUnclaimedTierAmounts, boxIds, expectedAmount, allowedAddress);
  }

  function test_claimDropBoxes_ClaimAndBurn() public {
    string memory code = "validCode";
    address allowedAddress = users.stranger;
    uint32 boxAmount = 5;
    uint256[] memory boxIds = new uint256[](boxAmount);
    uint256 earnmAmount = 1000 * 1e18;

    _setupClaimEnvironment(code, allowedAddress, boxAmount, boxIds, earnmAmount);
    (uint256 expectedAmount, uint256[TIER_IDS_ARRAY_LEN] memory expectedUnclaimedTierAmounts)
      = _calculateExpectedClaimAmount(boxIds);

    _fundAndClaim(allowedAddress, boxIds, 1 ether);
    _validateClaimedBoxes(expectedUnclaimedTierAmounts, boxIds, expectedAmount, allowedAddress);
  }
```

**Mode:**
Fixed in commit [82a2365](https://github.com/Earnft/dropbox-smart-contracts/commit/82a23652e1f806cfc10bafce389c8ef31ecf020a).

**Cyfrin:** Verified.
