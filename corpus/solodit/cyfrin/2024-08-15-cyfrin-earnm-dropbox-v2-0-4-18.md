---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-18
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Remove second `for` loop in `DropBox::claimDropBoxes` and reduce 1 storage
  read per deleted box
vuln_class: []
---

# Remove second `for` loop in `DropBox::claimDropBoxes` and reduce 1 storage read per deleted box

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** The first `for` loop inside `DropBox::claimDropBoxes` can be written like this such that the second `for` loop can be removed, meaning there is only need to iterate once over the input `_boxIds`:
```solidity
    for (uint256 i; i < _boxIds.length; i++) {
      // [Safety check] Duplicate values are not allowed
      if (i > 0 && _boxIds[i - 1] >= _boxIds[i]) revert BadRequest();

      // [Safety check] Validate that the box owner is the sender
      if (ownerOf(_boxIds[i]) != msg.sender) revert Unauthorized();

      // Copy the box from the boxes mapping
      Box memory box = boxIdToBox[_boxIds[i]];

      // Increment the amount of Earnm tokens to send to the sender
      amountToClaim += _calculateVestingPeriodPerBox(box.tier, box.blockTs, TIER_IDS_LENGTH);

      // Delete the box from the boxes mappings
      _deleteBox(_boxIds[i], box.tier);

      // Burn the ERC721 token corresponding to the box
      _burn(_boxIds[i]);
    }
```

The above code requires a modified `_deleteBox` function which saves 1 storage read per deleted box:
```solidity
  /// @param _boxTierId the tier id of the box to delete
  function _deleteBox(uint256 _boxId, uint128 _boxTierId) internal {
    // Delete from address -> _boxId mapping
    delete boxIdToBox[_boxId];

    // Decrease the unclaimed amount of boxes minted per tier
    unclaimedTierAmount[_boxTierId]--;
  }
```

This in turn requires 2 changes to the test suite to pass in the additional `_boxTierId` parameter:
```solidity
// mocks/DropBoxMock.sol
  function mock_deleteBox(uint256 boxId, uint128 tierId) public {
    _deleteBox(boxId, tierId);
  }

// DropBox/behaviors/boxStorage/deleteBox.t.sol
dropBox.mock_deleteBox(boxId, tierId);
```

**Mode:**
Fixed in commit [541f929](https://github.com/Earnft/dropbox-smart-contracts/commit/541f9297b5e0f072e8140d97f23031971e6fff21).

**Cyfrin:** Verified.
