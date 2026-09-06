---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Impossible to reveal any drop boxes linked to codes once enough codes have
  been associated such that `remainingBoxesAmount == 0`
vuln_class: []
---

# Impossible to reveal any drop boxes linked to codes once enough codes have been associated such that `remainingBoxesAmount == 0`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** In `DropBox::associateOneTimeCodeToAddress`, the `boxAmount` linked to allocated codes is deducted from `remainingBoxesAmount` storage:
```solidity
// Decrease the amount of boxes remaining to mint, since they are now associated to be minted
remainingBoxesAmount -= boxAmount;
```

Then in `DropBox::revealDropBoxes` when the user attempts to reveal the boxes previously linked with a code, if all the codes have been previously associated such that `remainingBoxesAmount == 0` the following safety checks cause the transaction to erroneously revert with `NoMoreBoxesToMint` error:
```solidity
// @audit read current `remainingBoxesAmount` from storage
// the box amount linked with this code has already been
// previously deducted in `associateOneTimeCodeToAddress`
uint256 remainingBoxesAmountCache = remainingBoxesAmount;

// @audit since the box amount linked with this code has
// already been deducted from `remainingBoxesAmount`, if
// all codes have been associated, even though not all codes have been
// revealed attempting to reveal any codes will erroneously revert since
// remainingBoxesAmountCache == 0
if (remainingBoxesAmountCache == 0) revert NoMoreBoxesToMint();

// @audit even if the previous check was removed, the transaction would
// still revert here since remainingBoxesAmountCache == 0 but
// oneTimeCodeData.boxAmount > 0
if (remainingBoxesAmountCache < oneTimeCodeData.boxAmount) revert NoMoreBoxesToMint();
```

**Impact:** Once all codes have been associated it is impossible to use any codes to reveal boxes. This makes it impossible to mint the remaining drop boxes linked to the associated but unrevealed codes and hence makes it impossible to claim the `EARNM` tokens associated with them.

**Proof of Concept:** Firstly in `test/DropBox/DropBox.t.sol` change the number of boxes such that there is only 1 box:
```diff
    dropBox = new DropBoxMock(
      address(users.operatorOwner),
      "https://api.example.com/",
      "https://api.example.com/contract",
      address(earnmERC20Token),
      address(users.apiAddress),
      [10_000_000, 1_000_000, 100_000, 10_000, 2500, 750],
-     [1, 10, 100, 1000, 2000, 6889],
+     [uint16(1), 0, 0, 0, 0, 0],
      ["Mythical Box", "Legendary Box", "Epic Box", "Rare Box", "Uncommon Box", "Common Box"],
      address(vrfHandler)
    );
```

Then add the PoC function to `test/DropBox/behaviors/revealDropBoxes.t.sol`:
```solidity
  function test_revealDropBoxes_ImpossibleToMintLastBox() public {
    string memory code = "validCode";
    uint32 boxAmount = 1;

    _setupAndAllowReveal(code, users.stranger, boxAmount);
    _mockVrfFulfillment(code, users.stranger, boxAmount);
    _validateMinting(dropBox.mock_getMintedTierAmounts(), boxAmount, code);
  }
```

Run the PoC with: `forge test --match-test test_revealDropBoxes_ImpossibleToMintLastBox -vvv`.

The PoC stack trace shows it fails to reveal the last and only box due to `[Revert] NoMoreBoxesToMint()` in `DropBoxMock::revealDropBoxes`.

Commenting out the `remainingBoxesAmountCache` checks in `DropBox::revealDropBoxes` then re-running the PoC shows that the last box can now be revealed.

**Recommended Mitigation:** Remove the `remainingBoxesAmountCache` checks from `DropBox::revealDropBoxes` since the boxes associated with codes are already deducted inside `DropBox::associateOneTimeCodeToAddress`.

**Mode:**
Fixed in commit [974fd2c](https://github.com/Earnft/dropbox-smart-contracts/commit/974fd2ce72b9e2d3c0355fdddb303c7c0146a692).

**Cyfrin:** Verified.

\clearpage
