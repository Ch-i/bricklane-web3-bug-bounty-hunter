---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-2-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_YLD_SplitMerge::merge` re-stamps the output NFT''s `hairCut` from the
  live registry instead of preserving the inputs'' agreed value, silently reclassifying
  the merged position into a new epoch and breaking merge compatibility with same-'
vuln_class: []
---

# `STBL_YLD_SplitMerge::merge` re-stamps the output NFT's `hairCut` from the live registry instead of preserving the inputs' agreed value, silently reclassifying the merged position into a new epoch and breaking merge compatibility with same-epoch peers

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_YLD_SplitMerge::merge` validates that both input NFTs carry the same `hairCut` before proceeding (lines 183–184). This check is by design: it ensures only compatible, same-epoch NFTs can be combined. After the check passes, however, the output NFT's `Fees` struct is populated via `_generateFeesStruct(metaA.assetID)` at line 204, which reads all fee fields — including `hairCut` — from the live registry at call time. The verified agreed value carried by both inputs is discarded.
```solidity
// STBL_YLD_SplitMerge.sol:183-184 — equality check (by design)
if (metaA.Fees.hairCut != metaB.Fees.hairCut)
    revert STBL_InvalidAsset(metaA.assetID, metaB.assetID);

// STBL_YLD_SplitMerge.sol:204 — output ignores the verified agreed value
Fees: _generateFeesStruct(metaA.assetID),
```

If an admin changed the registry's `hairCut` between the time the input NFTs were minted and the time `merge` is called, the output NFT silently receives the new `hairCut` even though both inputs carried the old one. The equality check confirmed the two inputs are from the same epoch; the output is stamped into a different epoch without any indication to the caller.
- `_generateFeesStruct` reads `hairCut` from the live registry unconditionally:
```solidity
// STBL_YLD_SplitMerge.sol:268-276
function _generateFeesStruct(uint256 _assetID) internal view returns (FeeStruct memory out) {
    AssetDefinition memory AssetData = registry.fetchAssetData(_assetID);
    out = FeeStruct({
        hairCut: AssetData.cut,  // live registry — not metaA.Fees.hairCut
        // ...
    });
}
```

**Impact:** The consequence appears in any subsequent merge operation. The merged NFT now carries the new-epoch `hairCut`. Any other NFT the owner holds from the same pre-change epoch still carries the old `hairCut`. Attempting to merge the output with such a peer fails at the equality check — `STBL_InvalidAsset` revert — because their `hairCut` values now differ. The owner has been silently reclassified into the new epoch mid-session and can no longer combine the merged position with remaining same-epoch holdings.

**Proof of Concept:**
1. NFT A and NFT B minted with `hairCut = 10`. Admin changes registry to `hairCut = 20`.
2. `merge(A, B)` — equality check passes (`10 == 10`). Output NFT minted with `Fees.hairCut = 20`.
3. Owner also holds NFT C from the same pre-change epoch (`hairCut = 10`).
4. `merge(output, C)` — equality check fails: `20 != 10` → `STBL_InvalidAsset` revert.
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/// @title  Merge Output NFT hairCut Re-Stamped From Live Registry
/// @notice merge() re-stamps the output NFT's hairCut from the live registry instead of
///         preserving the inputs' agreed value. Two NFTs with hairCut=10 are successfully
///         merged after the admin changes the registry to hairCut=20; the output NFT silently
///         carries hairCut=20. The merged position is then incompatible with any remaining
///         same-epoch (hairCut=10) NFTs.
/// @dev    Root cause: STBL_YLD_SplitMerge.merge() line 204 uses _generateFeesStruct()
///         (live registry read) instead of metaA.Fees to populate the output Fees struct.
///         Fix: replace _generateFeesStruct(metaA.assetID) with metaA.Fees at line 204.
/// @author 0xStalin

/// Run: cd stbl-contracts-evm-redemptions && forge test --match-test test_poc_mergeOutputHairCutReStampedFromRegistry -vvv

import "forge-std/Test.sol";
import "forge-std/console.sol";
import {Helper} from "./helper.t.sol";
import {STBL_YLD_SplitMerge} from "../contracts/splitter/STBL_YLD_SplitMerge.sol";
import {STBL_PT1_Issuer} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/issuers/STBL_PT1_Issuer.sol";
import {STBL_TestToken} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/test/STBL_TestToken.sol";
import {STBL_InvalidAsset} from "../contracts/lib/STBL_Errors.sol";

contract MergeHairCutReStamp_PoC is Helper {
    STBL_YLD_SplitMerge public splitMerge;

    uint256 constant ASSET_SLOT = 1;
    uint256 constant DEPOSIT = 10_000 * 1e18;
    uint256 constant INITIAL_HAIRCUT = 10;
    uint256 constant NEW_HAIRCUT = 20;

    uint256 public assetRegID;

    function setUp() public override {
        super.setUp();

        deployAsset(ASSET_SLOT, AssetType.PT1);
        assetRegID = getAssetRegistryId(ASSET_SLOT);

        vm.startPrank(admin);

        // user1 needs tokens for two deposits (NFT A and NFT B)
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mintVal(user1, 2 * DEPOSIT);
        // user2 needs tokens for one deposit (NFT C)
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mintVal(user2, DEPOSIT);

        // Deploy SplitMerge, grant MINTER_ROLE on YLD and SPLITTER_ROLE on registry
        splitMerge = new STBL_YLD_SplitMerge(address(registry));
        yld.grantRole(yld.MINTER_ROLE(), address(splitMerge));
        registry.grantRole(keccak256("SPLITTER_ROLE"), address(splitMerge));

        vm.stopPrank();
    }

    // Issue a YLD NFT to `_user` by depositing `_amount` via the PT1 Issuer.
    function _issueNFT(address _user, uint256 _amount) internal returns (uint256 nftId) {
        vm.startPrank(_user);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).approve(getAssetVault(ASSET_SLOT), _amount);
        nftId = STBL_PT1_Issuer(getAssetIssuer(ASSET_SLOT)).deposit(_amount);
        vm.stopPrank();
    }

    /// @notice PoC: merge() silently re-stamps the output NFT's hairCut from the live registry,
    ///         breaking compatibility with remaining same-epoch peers.
    function test_poc_mergeOutputHairCutReStampedFromRegistry() public {

        // == [ Phase 1: Mint NFT A and NFT B for user1 (hairCut = INITIAL_HAIRCUT = 10) ] ==

        uint256 nftA = _issueNFT(user1, DEPOSIT);
        uint256 nftB = _issueNFT(user1, DEPOSIT);

        console.log("--- Phase 1: user1 mints NFT A and NFT B ---");
        console.log("NFT A ID:", nftA, "  hairCut:", yld.getNFTData(nftA).Fees.hairCut);
        console.log("NFT B ID:", nftB, "  hairCut:", yld.getNFTData(nftB).Fees.hairCut);

        assertEq(yld.getNFTData(nftA).Fees.hairCut, INITIAL_HAIRCUT, "pre-condition: NFT A must have INITIAL_HAIRCUT");
        assertEq(yld.getNFTData(nftB).Fees.hairCut, INITIAL_HAIRCUT, "pre-condition: NFT B must have INITIAL_HAIRCUT");

        // == [ Phase 2: Mint NFT C for user2 — same epoch, hairCut = 10 ] ==

        uint256 nftC = _issueNFT(user2, DEPOSIT);

        console.log("--- Phase 2: user2 mints NFT C (same epoch, hairCut = 10) ---");
        console.log("NFT C ID:", nftC, "  hairCut:", yld.getNFTData(nftC).Fees.hairCut);

        assertEq(yld.getNFTData(nftC).Fees.hairCut, INITIAL_HAIRCUT, "pre-condition: NFT C must have INITIAL_HAIRCUT");

        // == [ Phase 3: Admin changes registry hairCut from 10 to 20 ] ==

        console.log("--- Phase 3: Admin sets registry hairCut ---");
        console.log("  from:", INITIAL_HAIRCUT, "to:", NEW_HAIRCUT);

        vm.prank(admin);
        registry.setCut(assetRegID, NEW_HAIRCUT);

        console.log("Registry hairCut after setCut:", registry.fetchAssetData(assetRegID).cut);
        // NFTs on-chain are unaffected until a merge/split touches them
        console.log("NFT A hairCut (unchanged on-chain):", yld.getNFTData(nftA).Fees.hairCut);
        console.log("NFT B hairCut (unchanged on-chain):", yld.getNFTData(nftB).Fees.hairCut);

        // == [ Phase 4: user1 merges NFT A + NFT B — equality check passes (10 == 10) ] ==

        console.log("--- Phase 4: user1 merges NFT A and NFT B ---");
        console.log("Inputs both carry hairCut =", INITIAL_HAIRCUT, "-- equality check must pass");

        vm.startPrank(user1);
        yld.approve(address(splitMerge), nftA);
        yld.approve(address(splitMerge), nftB);
        uint256 mergedNFT = splitMerge.merge(nftA, nftB);
        vm.stopPrank();

        uint256 mergedHairCut = yld.getNFTData(mergedNFT).Fees.hairCut;
        console.log("Merged NFT ID:", mergedNFT);
        console.log("Merged NFT hairCut: expected", NEW_HAIRCUT, "input was", INITIAL_HAIRCUT);
        console.log("  actual merged hairCut:", mergedHairCut);

        // == [ Phase 5: Assert exploit — merged output carries live-registry hairCut, not inputs' value ] ==

        console.log("--- Phase 5: Exploit assertions ---");

        // Bug confirmed: merged NFT carries the NEW registry hairCut, not the inputs' agreed value
        assertEq(
            mergedHairCut,
            NEW_HAIRCUT,
            "exploit: merged NFT must carry live-registry hairCut"
        );
        // Invariant violation: inputs' hairCut is silently discarded
        assertNotEq(
            mergedHairCut,
            INITIAL_HAIRCUT,
            "exploit: merged NFT must NOT preserve inputs' hairCut"
        );

        console.log("[+] EXPLOIT CONFIRMED: merge() re-stamped output hairCut from registry");
        console.log("  registry hairCut:", NEW_HAIRCUT, "  inputs hairCut:", INITIAL_HAIRCUT);

        // == [ Phase 6: Secondary impact — mergedNFT is incompatible with same-epoch peer NFT C ] ==

        console.log("--- Phase 6: Transfer NFT C to user1, attempt merge(mergedNFT, C) --- expect revert ---");
        console.log("Merged NFT hairCut:", mergedHairCut, "  NFT C hairCut:", yld.getNFTData(nftC).Fees.hairCut);

        vm.prank(user2);
        yld.transferFrom(user2, user1, nftC);

        vm.startPrank(user1);
        yld.approve(address(splitMerge), mergedNFT);
        yld.approve(address(splitMerge), nftC);

        // hairCut mismatch at line 184 of merge() fires: metaA.hairCut (20) != metaB.hairCut (10)
        // (assetID equality at line 181 passes since both NFTs share the same assetRegID)
        vm.expectRevert(
            abi.encodeWithSelector(STBL_InvalidAsset.selector, assetRegID, assetRegID)
        );
        splitMerge.merge(mergedNFT, nftC);

        vm.stopPrank();

        console.log("[+] SECONDARY IMPACT CONFIRMED: merge(mergedNFT, C) reverts with STBL_InvalidAsset --", NEW_HAIRCUT, "!=", INITIAL_HAIRCUT);
        console.log("[+] Same-epoch NFT C is permanently incompatible with the re-stamped merged position");
    }
}
```

**Recommended Mitigation:** Replace `_generateFeesStruct(metaA.assetID)` with `metaA.Fees` at the `Fees:` field of the merged output struct in `merge`. The equality check at lines 183–184 already guarantees both inputs carry the same fee snapshot, so the output can inherit `metaA.Fees` directly. No registry read is needed at this point, and the merged NFT remains compatible with same-epoch peers for all subsequent operations.

**STBL:** Fixed in commits [59953ff](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/59953ff4d603ed4be0f68d5a175b4e659d714553) && [9315f68](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/9315f68b79442e96f16d7ffc764c184d7a1f46a1).

**Cyfrin:** Verified. `STBL_YLD_SplitMerge` now preserve the inputs' agreed `hairCut` on the merged output by overriding `merged.Fees.hairCut = metaA.Fees.hairCut` after the `_generateFeesStruct` call, discarding the live-registry value in favour of the epoch snapshot both inputs carried
