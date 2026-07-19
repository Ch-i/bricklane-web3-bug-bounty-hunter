---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-17
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Cache result of `_getOneTimeCodeHash` to prevent repeated identical calculation
  in `DropBox::associateOneTimeCodeToAddress`
vuln_class: []
---

# Cache result of `_getOneTimeCodeHash` to prevent repeated identical calculation in `DropBox::associateOneTimeCodeToAddress`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `DropBox::associateOneTimeCodeToAddress` currently calculates `_getOneTimeCodeHash(code, allowedAddress)` twice:
```solidity
    // [Safety check] Validate that the one-time code is not already associated to an address
    // @audit 1) calculating _getOneTimeCodeHash for first time
    address claimerAddress = oneTimeCode[_getOneTimeCodeHash(code, allowedAddress)].claimer;
    if (claimerAddress != address(0x0)) revert OneTimeCodeAlreadyAssociated(claimerAddress);

    // [Safety check] Validate that the one-time code has not been used
    if (oneTimeCodeUsed[keccak256(bytes(code))]) revert OneTimeCodeAlreadyUsed();

    uint256 remainingBoxesAmountCache = remainingBoxesAmount;

    // [Safety check] Validate that there are still balance of boxes to mint
    if (remainingBoxesAmountCache == 0) revert NoMoreBoxesToMint();

    // [Safety check] Validate that the remaining boxes to mint are greater or equal to the box amount
    if (remainingBoxesAmountCache < boxAmount) revert NoMoreBoxesToMint();
    // ---------------------------------------------------------------------------------------------

    // Decrease the amount of boxes remaining to mint, since they are now associated to be minted
    remainingBoxesAmount -= boxAmount;

    // Generate the hash of the code and the sender address
    // @audit 2) calculating _getOneTimeCodeHash again with identical inputs
    bytes32 otpHash = _getOneTimeCodeHash(code, allowedAddress);
```

Since `code` and `allowedAddress` don't change there is no point recalculating again; simply do it once and used the cached result:
```diff
+   // Generate the hash of the code and the sender address
+   bytes32 otpHash = _getOneTimeCodeHash(code, allowedAddress);

    // [Safety check] Validate that the one-time code is not already associated to an address
-   address claimerAddress = oneTimeCode[_getOneTimeCodeHash(code, allowedAddress)].claimer;
+   address claimerAddress = oneTimeCode[otpHash].claimer;
    if (claimerAddress != address(0x0)) revert OneTimeCodeAlreadyAssociated(claimerAddress);

    // [Safety check] Validate that the one-time code has not been used
    if (oneTimeCodeUsed[keccak256(bytes(code))]) revert OneTimeCodeAlreadyUsed();

    uint256 remainingBoxesAmountCache = remainingBoxesAmount;

    // [Safety check] Validate that there are still balance of boxes to mint
    if (remainingBoxesAmountCache == 0) revert NoMoreBoxesToMint();

    // [Safety check] Validate that the remaining boxes to mint are greater or equal to the box amount
    if (remainingBoxesAmountCache < boxAmount) revert NoMoreBoxesToMint();
    // ---------------------------------------------------------------------------------------------

    // Decrease the amount of boxes remaining to mint, since they are now associated to be minted
    remainingBoxesAmount -= boxAmount;

-   // Generate the hash of the code and the sender address
-   bytes32 otpHash = _getOneTimeCodeHash(code, allowedAddress);
```

**Mode:**
Fixed in commit [1c983c2](https://github.com/Earnft/dropbox-smart-contracts/commit/1c983c2597be511b22fad5a33ee45bcce000dada).

**Cyfrin:** Verified.
