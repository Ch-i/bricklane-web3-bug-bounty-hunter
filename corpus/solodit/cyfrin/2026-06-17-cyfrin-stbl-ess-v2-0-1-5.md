---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-1-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_ESS_NFT_Vault1::_Vault_mergeLot` skips yield claim before NFT burn,
  permanently stranding accrued rewards in the `YieldDistributor`'
vuln_class: []
---

# `STBL_ESS_NFT_Vault1::_Vault_mergeLot` skips yield claim before NFT burn, permanently stranding accrued rewards in the `YieldDistributor`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_ESS_NFT_Vault1::_Vault_mergeLot` merges two lot NFT pairs by delegating to `STBL_YLD_SplitMerge::merge` without first calling `_Vault_claimYield` on either lot.
Inside `STBL_YLD_SplitMerge::merge`, both input NFTs are **burned before** yield staking is disabled:

```solidity
YLD.burn(caller, _tokenIdA);   // sets isDisabled = true in NFT metadata
YLD.burn(caller, _tokenIdB);
newTokenId = YLD.mint(caller, merged);

iSTBL_Issuer(assetData.issuer).disableYield(_tokenIdA);
iSTBL_Issuer(assetData.issuer).disableYield(_tokenIdB);
iSTBL_Issuer(assetData.issuer).enableYield(newTokenId);
```

`disableYield` calls `YieldDistributor::disableStaking`, which runs `_updateRewards` before zeroing the staking balance. `_updateRewards` snapshots all accrued pending rewards into `stakingData[id].earned` — but does not transfer them. **The yield is now sitting in the distributor under the burned token's ID.**

**Impact:** After the merged NFTs get burned, every attempt to retrieve those rewards via `claim(burnedId)` is permanently blocked. `iClaim` reads the NFT metadata and finds `isDisabled == true`(set by `YLD::burn`), then reverts with `STBL_YLDDisabled`. **The reward tokens are locked in the `YieldDistributor`'s ERC-20 balance.**

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./XLayer_Setup.sol";
import {iSTBL_ESS_NFT_Vault1} from "../contracts/interfaces/ISTBL_ESS_NFT_Vault1.sol";

/**
 * @title MergeLotYieldLoss_PoC
 * @notice Proof-of-concept confirming that mergeLot permanently strands accrued yield on
 *         all NFTs belonging to the merged input lots.
 * @dev Root cause: STBL_YLD_SplitMerge.merge() burns both input NFTs (sets
 *      MetaData.isDisabled = true) BEFORE calling disableYield() on them.
 *      disableYield -> disableStaking snapshots stakingData[id].earned but never
 *      transfers those rewards. After the burn, every claim(burnedId) reverts with
 *      STBL_YLDDisabled(burnedId) because iClaim checks MetaData.isDisabled == true
 *      first. The rewards are permanently stranded — no recovery path exists.
 *
 *      Correct pattern: STBL_UT1e_Issuer.iWithdraw calls claim BEFORE disableStaking.
 *
 * @author 0xStalin
 */
contract MergeLotYieldLoss_PoC is XLayer_Setup {
    uint256 constant DEPOSIT = 100_000 * 1e18;

    function setUp() public override {
        super.setUp();
        mintTestTokensToUser(user1, DEPOSIT * 2);
        approveWrapperForUser(user1);
    }

    /// @notice PoC: mergeLot strands accrued yield on burned NFTs permanently
    /// Title:    Missing yield claim before NFT burn in merge path causes permanent yield loss
    /// Affected: STBL_ESS_NFT_Vault1._Vault_mergeLot, STBL_YLD_SplitMerge.merge
    /// Impact:   Any lot owner who calls mergeLot loses all accrued yield on all NFTs in
    ///           both input lots. No elevated privileges required.
    /// Author:   0xStalin
    function test_poc_mergeLot_strandsYieldOnBurnedNFTs() public {
        // == [ Setup ] ==

        // user1 deposits twice to obtain two separate lots
        vm.prank(user1);
        uint256 lotA = xLayerWrapper.ess_deposit(DEPOSIT);

        vm.prank(user1);
        uint256 lotB = xLayerWrapper.ess_deposit(DEPOSIT);

        // Capture the asset1 NFT ID from lotA — yieldDistributor1 tracks this token
        iSTBL_ESS_NFT_Vault1.lotStruct memory lotData = xLayerNFTVault.fetchLotDetails(lotA);
        uint256 nftId = lotData.ids[0];

        console.log("=== PoC: mergeLot strands accrued yield on burned NFTs ===");
        console.log("[*] lotA:", lotA, "  lotB:", lotB);
        console.log("[*] Tracking asset1 NFT ID from lotA:", nftId);

        // == [ Generate Yield ] ==

        // Advance oracle prices so yield accrues, then distribute
        increaseAsset1Price();
        increaseAsset2Price();
        vm.warp(block.timestamp + 2 days);

        vm.prank(address(xLayerWrapper));
        vault1.distributeYield();

        vm.prank(address(xLayerWrapper));
        vault2.distributeYield();

        // Pre-merge: confirm the NFT has non-zero earned rewards
        uint256 earnedBeforeMerge = yieldDistributor1.calculateRewardsEarned(nftId);
        console.log("[*] Earned rewards on NFT before merge:", earnedBeforeMerge);
        assertGt(earnedBeforeMerge, 0, "Pre-condition: yield must have accrued before merge");

        // == [ Execute Merge ] ==

        // user1 merges the two lots — this call succeeds (the bug is silent)
        vm.prank(user1);
        uint256 mergedLot = xLayerNFTVault.mergeLot(lotA, lotB);

        // Capture the new merged NFT ID — this is what should have received the yield
        iSTBL_ESS_NFT_Vault1.lotStruct memory mergedLotData = xLayerNFTVault.fetchLotDetails(mergedLot);
        uint256 mergedNftId = mergedLotData.ids[0];

        console.log("[*] mergeLot(lotA, lotB) completed without revert");
        console.log("[*] New merged lot:", mergedLot, "  merged asset1 NFT ID:", mergedNftId);

        // == [ Verify Impact ] ==

        // The stranded yield is still visible via the view function — it was snapshotted
        // by disableStaking but can never be transferred because claim is now blocked.
        uint256 earnedAfterMerge = yieldDistributor1.calculateRewardsEarned(nftId);
        console.log("[*] Earned rewards on burned NFT after merge (stranded):", earnedAfterMerge);
        assertGt(earnedAfterMerge, 0, "Yield must still be recorded as earned (stranded, not zeroed)");

        // The merged NFT starts fresh — it did NOT inherit the stranded yield from either input NFT.
        // enableYield(mergedNftId) sets stakingData[mergedNftId].rewardIndex = currentIndex,
        // so earned = 0 and no historical rewards are forwarded.
        uint256 earnedOnMergedNft = yieldDistributor1.calculateRewardsEarned(mergedNftId);
        console.log("[*] Earned rewards on NEW merged NFT (expected 0):", earnedOnMergedNft);
        assertEq(earnedOnMergedNft, 0, "Merged NFT must start with zero yield - stranded rewards were not forwarded");

        // Attempting to claim the stranded rewards must revert with STBL_YLDDisabled
        // because merge burned the NFT (set MetaData.isDisabled = true) before disableYield
        // had a chance to transfer the rewards.
        console.log("[*] Attempting claim on burned NFT - expected revert: STBL_YLDDisabled");
        vm.expectRevert(abi.encodeWithSelector(STBL_YLDDisabled.selector, nftId));
        yieldDistributor1.claim(nftId);

        console.log("[+] CONFIRMED: burned NFT yield is stranded and unreachable");
        console.log("[+] CONFIRMED: merged NFT received 0 yield - rewards permanently lost");
        console.log("[+] Stranded yield amount:", earnedAfterMerge);
    }
}
```

**Recommended Mitigation:** Call `_Vault_claimYield` for both input lots inside `STBL_ESS_NFT_Vault1._Vault_mergeLot`before delegating to `STBL_YLD_SplitMerge::merge`.
This mirrors the claim-first ordering already applied in `STBL_UT1e_Issuer.iWithdraw`.

**STBL:** Fixed in commit [4a7ed80](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/4a7ed809e053d739cd47c4c3a283988b2076a751).

**Cyfrin:** Verified. `_Vault_mergeLot` now calls `_Vault_claimYield` on both input lots before delegating to `SplitMerge::merge`, ensuring all accrued rewards are harvested before the NFTs are burned.
