---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: LP yield permanently orphaned in `STBL_Redemption_Core::iWithdraw` and `STBL_Redemption_Core::iRedeem`
  due to missing `iClaimYield` before pool NFT split
vuln_class: []
---

# LP yield permanently orphaned in `STBL_Redemption_Core::iWithdraw` and `STBL_Redemption_Core::iRedeem` due to missing `iClaimYield` before pool NFT split

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_Redemption_Core` holds a single pooled YLD NFT (`NFTID`) representing all LP deposits. Yield accrues continuously on this NFT inside the external `YieldDistributor`, keyed by the NFT's token ID.
`STBL_Redemption_Core::iClaimYield` pulls that yield into the pool by calling `YieldDistributor.claim(NFTID)` and incrementing the internal `rewardIndex`; this is the only mechanism by which yield reaches LP shareholders.

Neither `iWithdraw` nor `iRedeem` calls `iClaimYield` before invoking `spliter.split(NFTID, _amt)`. Inside `split`, the old `NFTID` is burned, and two new NFTs are minted. The splitter then calls `iSTBL_Issuer.disableYield(oldNFTID)`, which reaches `disableStaking(oldNFTID)` on the `YieldDistributor`.
`disableStaking` snapshots pending yield into `stakingData[oldNFTID].earned` but does **not** call `claim`.
After the burn, `YToken.ownerOf(oldNFTID)` reverts on any subsequent call, so `YieldDistributor.claim(oldNFTID)` can never succeed again. The unclaimed yield is therefore stranded.

Step-by-Step:
1. LP calls `withdraw(_amt)` -> `iWithdraw(_amt)`.
2. `_updateRewards(msg.sender)` updates the LP's internal reward accounting against the current (stale) `rewardIndex`. This does **not** pull new yield from the distributor; it only snapshots already-ingested yield.
3. `spliter.split(NFTID, _amt)` is called. Inside `split()`:
   - `YLD.burn(caller, oldNFTID)` — the old pool NFT is destroyed.
   - `tokenIdA` and `tokenIdB` are minted.
   - `iSTBL_Issuer.disableYield(oldNFTID)` -> `disableStaking(oldNFTID)`: snapshots yield into `stakingData[oldNFTID].earned`, zeroes the staking balance. No `claim()` is issued, no tokens are transferred.
   - `iSTBL_Issuer.enableYield(tokenIdA/B)`: registers the new NFTs from a zero starting balance.
4. `NFTID = tokenIdA`. All yield accrued under `oldNFTID` since the last `iClaimYield()` is now stored in `stakingData[oldNFTID].earned`, keyed to a burned token. It can never enter the pool's `rewardIndex`.

The sequence is identical in `iRedeem`. Note that `iRedeem` does call `issuer.withdraw(_B)` on `tokenIdB`, which internally triggers a `claim` on that piece — but this only captures yield for the redeemer's split fragment, not the pool's share of pre-split yield that was stranded under the old `NFTID`.

**Impact:** Every call to `STBL_Redemption::withdraw` or `STBL_Redemption::redeem` is affected whenever any yield has accrued since the last `claimYield` call. No special privileges are required; both functions are permissionless public entry points exercised in routine operation. The loss is permanent and compounds over the pool's lifetime.

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/**
 * @title  YieldOrphaned_PoC
 * @notice PoC: LP yield permanently orphaned on every LP withdrawal due to missing iClaimYield() before split
 * @dev    Title:    LP yield permanently orphaned in iWithdraw due to missing iClaimYield() before pool NFT split
 *         Affected: STBL_Redemption_Core.sol:137-157 (iWithdraw), 172-202 (iRedeem)
 *         Impact:   Pending yield silently orphaned under the dead NFT ID on every withdrawal - LPs forfeit yield
 *         Author:   0xStalin
 */

import "forge-std/Test.sol";
import "forge-std/console.sol";

import {Helper} from "./helper.t.sol";

import {STBL_YLD_SplitMerge} from "../contracts/splitter/STBL_YLD_SplitMerge.sol";
import {STBL_Redemption} from "../contracts/redemption/STBL_Redemption.sol";
import {STBL_Redemption_Core} from "../contracts/redemption/STBL_Redemption_Core.sol";

import {STBL_PT1_Issuer} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/issuers/STBL_PT1_Issuer.sol";
import {STBL_T1_YieldDistributor} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/yielddistributor/STBL_T1_YieldDistributor.sol";
import {STBL_TestToken} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/test/STBL_TestToken.sol";
import {STBL_TestOracle} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/test/STBL_TestOracle.sol";
import {STBL_T1_Vault} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/vault/STBL_T1_Vault.sol";

import "@stbl-protocol/stbl-contracts-evm-core/contracts/lib/STBL_Structs.sol";

// ─────────────────────────────────────────────────────────────────────────────
//  Thin wrapper that exposes internal state for PoC assertions.
//  Adds getRewardIndex() on top of the existing helpers.
// ─────────────────────────────────────────────────────────────────────────────
contract InspectableRedemptionPoC is STBL_Redemption {
    constructor(address _register, address _splitter, uint256 _assetID)
        STBL_Redemption(_register, _splitter, _assetID) {}

    function getNFTID() external view returns (uint256) { return NFTID; }
    function getTotalSupply() external view returns (uint256) { return totalSupply; }
    function getRewardIndex() external view returns (uint256) { return rewardIndex; }
    function getUserData(address _user) external view returns (uint256 stableValueNet, uint256 rewardIdx, uint256 earned) {
        RedepmtionStruct memory d = userData[_user];
        return (d.stableValueNet, d.rewardIndex, d.earned);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  PoC Test Suite
// ─────────────────────────────────────────────────────────────────────────────
contract YieldOrphaned_PoC is Helper {
    // ── Contracts under test ─────────────────────────────────────────────
    STBL_YLD_SplitMerge public splitMerge;
    InspectableRedemptionPoC public redemption;

    // ── Single asset (slot index 1) ──────────────────────────────────────
    uint256 constant ASSET_SLOT = 1;
    uint256 public assetRegID;

    uint256 constant DEPOSIT = 10_000 * 1e18;

    // ─────────────────────────────────────────────────────────────────────
    //  setUp
    // ─────────────────────────────────────────────────────────────────────
    function setUp() public override {
        super.setUp(); // deploys core: USST, YLD, Registry, Core

        // Deploy one PT1 asset
        deployAsset(ASSET_SLOT, AssetType.PT1);
        assetRegID = getAssetRegistryId(ASSET_SLOT);

        // Fund user1 with underlying asset tokens
        vm.startPrank(admin);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user1);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user1);

        // Deploy SplitMerge, grant MINTER_ROLE on YLD and SPLITTER_ROLE on registry
        splitMerge = new STBL_YLD_SplitMerge(address(registry));
        yld.grantRole(yld.MINTER_ROLE(), address(splitMerge));
        registry.grantRole(keccak256("SPLITTER_ROLE"), address(splitMerge));

        // Deploy the redemption contract (wrapped for state inspection)
        redemption = new InspectableRedemptionPoC(
            address(registry),
            address(splitMerge),
            assetRegID
        );
        vm.stopPrank();
    }

    // ─────────────────────────────────────────────────────────────────────
    //  Helpers (mirrored from Redemption.t.sol, independent copy)
    // ─────────────────────────────────────────────────────────────────────

    function _issueNFT(address _user, uint256 _amount) internal returns (uint256 nftId) {
        vm.startPrank(_user);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).approve(getAssetVault(ASSET_SLOT), _amount);
        nftId = STBL_PT1_Issuer(getAssetIssuer(ASSET_SLOT)).deposit(_amount);
        vm.stopPrank();
    }

    function _skipLockPeriod() internal {
        vm.warp(block.timestamp + 10_000_001);
        vm.roll(block.number + 1);
    }

    // ─────────────────────────────────────────────────────────────────────
    //  PoC: yield orphaned on withdrawal without prior claimYield()
    // ─────────────────────────────────────────────────────────────────────
    function test_poc_yieldOrphanedOnWithdraw() public {

        // == [ Setup ] ==

        // user1 issues a YLD NFT and deposits it into the redemption pool
        uint256 userNft = _issueNFT(user1, DEPOSIT);

        vm.startPrank(user1);
        yld.approve(address(redemption), userNft);
        redemption.deposit(userNft);
        vm.stopPrank();

        // Capture pool NFT ID after deposit
        uint256 poolNFTID = redemption.getNFTID();
        console.log("--- Setup ---");
        console.log("Pool NFTID after deposit:", poolNFTID);

        // == [ Generate Yield ] ==

        // Advance time past yieldDuration so distributeYield succeeds
        _skipLockPeriod();

        vm.startPrank(admin);
        STBL_TestOracle(getAssetOracle(ASSET_SLOT)).setPrice();
        STBL_T1_Vault(getAssetVault(ASSET_SLOT)).distributeYield();
        vm.stopPrank();

        // == [ Pre-Withdrawal State ] ==

        STBL_T1_YieldDistributor distributor =
            STBL_T1_YieldDistributor(getAssetYieldDistributor(ASSET_SLOT));

        uint256 pendingYieldBefore = distributor.calculateRewardsEarned(poolNFTID);

        console.log("--- Pre-Withdrawal State ---");
        console.log("Pool NFTID:", poolNFTID);
        console.log("Pending yield in distributor for pool NFT:", pendingYieldBefore);
        console.log("Pool rewardIndex before withdrawal:", redemption.getRewardIndex());

        // Confirm yield actually exists - otherwise the PoC premise fails
        assertGt(pendingYieldBefore, 0, "setup: yield must exist before withdrawal");

        // Determine halfAmt: must satisfy 0 < halfAmt < stableValueNet
        YLD_Metadata memory poolMeta = yld.getNFTData(poolNFTID);
        uint256 halfAmt = poolMeta.stableValueNet / 2;
        assertGt(halfAmt, 0, "setup: halfAmt must be > 0");

        // == [ Execute Withdrawal Without claimYield ] ==

        // user1 withdraws half their share without first calling claimYield().
        // Internally iWithdraw calls spliter.split(NFTID, halfAmt) which burns
        // the old NFTID and calls disableYield(oldNFTID) -> disableStaking(oldNFTID).
        // disableStaking snapshots earned yield into stakingData[oldNFTID].earned
        // but never transfers it. After the burn, ownerOf(oldNFTID) reverts,
        // making claim(oldNFTID) permanently impossible.
        uint256 oldNFTID = poolNFTID;

        vm.prank(user1);
        redemption.withdraw(halfAmt);

        uint256 newNFTID = redemption.getNFTID();

        // Sanity: confirm split actually happened (IDs must differ)
        assertNotEq(oldNFTID, newNFTID, "split: pool NFTID must change after withdrawal");

        console.log("--- Post-Withdrawal State ---");
        console.log("Old (now burned) pool NFTID:", oldNFTID);
        console.log("New pool NFTID:", newNFTID);
        console.log("Orphaned yield under dead NFT ID:", distributor.calculateRewardsEarned(oldNFTID));
        console.log("Pool rewardIndex after withdrawal:", redemption.getRewardIndex());

        // == [ Verify Impact ] ==

        // calculateRewardsEarned reads only from the stakingData mapping (no ownerOf call),
        // so it remains callable even after the NFT is burned. The mapping data persists;
        // only the NFT ownership is erased. The earned value was snapshotted by disableStaking
        // but never claimed, so it remains exactly as large as it was before the split.
        // The orphaned yield is still stored under the dead NFT ID - unchanged
        assertEq(
            distributor.calculateRewardsEarned(oldNFTID),
            pendingYieldBefore,
            "orphaned: yield stranded under burned NFT ID unchanged"
        );

        // The pool's rewardIndex was never updated - yield never flowed into the pool
        assertEq(
            redemption.getRewardIndex(),
            0,
            "orphaned: pool rewardIndex is still zero - yield never entered the pool"
        );

        // Calling claimYield() after the withdrawal captures nothing for the new NFTID
        redemption.claimYield();

        console.log("--- After claimYield() on new NFTID ---");
        console.log("Pool rewardIndex after claimYield():", redemption.getRewardIndex());

        assertEq(
            redemption.getRewardIndex(),
            0,
            "orphaned: claimYield() on the new NFTID returns 0 - the yield was lost at split time"
        );

        console.log("[+] CONFIRMED: yield orphaned under dead NFT ID - pool rewardIndex never updated");
    }
}
```

**Recommended Mitigation:** Call `iClaimYield` at the top of `iWithdraw` and `iRedeem`, before the `spliter.split(NFTID, _amt)` call, so all pending yield is captured into the pool's `rewardIndex` before the pool NFT is burned and replaced.

**STBL:** Fixed in commit [cd80dd4](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/cd80dd4a5d9e281d7ce9411c8fc7f214484e4a21).

**Cyfrin:** Verified. Both `iWithdraw` and `iRedeem` now call `iClaimYield` at the top of the function, before `spliter::split` is invoked. This ensures all pending distributor yield is flushed into `rewardIndex` while the pool NFT is still alive and claimable, so existing LPs capture their proportional share before the old NFT is burned and replaced by the split.
