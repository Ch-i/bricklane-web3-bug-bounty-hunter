---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-2-0
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
title: Depositor's pre-deposit yield permanently lost in `STBL_Redemption_Core::iDeposit`
  as merge burns incoming YLD NFT before yield is claimed
vuln_class: []
---

# Depositor's pre-deposit yield permanently lost in `STBL_Redemption_Core::iDeposit` as merge burns incoming YLD NFT before yield is claimed

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_Redemption_Core::iDeposit` accepts a depositor's YLD NFT and, when the pool already holds a NFT (`NFTID != 0`), merges the incoming NFT into the pool via `spliter.merge(NFTID, _id)`. The merge operation in `STBL_YLD_SplitMerge` burns both constituent NFTs and calls `disableYield(_id)` on the incoming one.

`disableYield` snapshots any pending distributor yield into `stakingData[_id].earned`, then the NFT is burned. Because `_id` no longer exists after the burn, `distributor.claim(_id)` permanently reverts on `YLD.ownerOf(_id)` — the snapshotted yield is trapped in storage with no recovery path.

`STBL_Redemption_Core::iDeposit` does not call `distributor.claim(_id)` (or any equivalent flush) on the incoming NFT before the merge. There is no warning, guard, or documentation that alerts the depositor to this condition. Any yield that has accrued for their NFT in the `YieldDistributor` between the last distribution and the moment the depositors call `STBL_Redemption::deposit` is irrecoverably lost.

```solidity
function iDeposit(uint256 _id) internal {
    _updateRewards(msg.sender);
    // ...
    YLD.transferFrom(msg.sender, address(this), _id);
    if (NFTID == 0) {
        NFTID = _id;
    } else {
        NFTID = spliter.merge(NFTID, _id);  // burns _id, trapping its pending yield
    }
    // ...
}
```

**Impact:** Affects every depositor whose NFT has accumulated unclaimed yield — the normal state for any NFT held across a yield distribution cycle. The loss can occur in normal usage.

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
contract InspectableRedemption4 is STBL_Redemption {
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
//  Vulnerability: iDeposit() calls spliter.merge(NFTID, _id) which burns _id
//  via YLD.burn(_id) and then calls disableYield(_id). disableYield() snapshots
//  any pending distributor yield into stakingData[_id].earned. Because _id is
//  already burned at that point, distributor.claim(_id) permanently reverts
//  (ownerOf(_id) reverts on a burned token). The depositor's accumulated yield
//  is irrecoverably trapped in dead storage.
//
//  Net impact: Every depositor whose NFT gets merged permanently loses ALL
//  pending distributor yield that had accrued on their NFT up to that point.
//  No principal is lost — only yield is lost.
// ─────────────────────────────────────────────────────────────────────────────
contract DepositorYieldLost_PoC is Helper {
    // Contracts under test
    STBL_YLD_SplitMerge public splitMerge;
    InspectableRedemption4 public redemption;

    uint256 constant ASSET_SLOT = 1;
    uint256 constant DEPOSIT = 10_000 * 1e18;

    uint256 public assetRegID;

    function setUp() public override {
        super.setUp();

        deployAsset(ASSET_SLOT, AssetType.PT1);
        assetRegID = getAssetRegistryId(ASSET_SLOT);

        vm.startPrank(admin);

        // Fund user1 (seed LP — establishes a non-empty pool) and user2 (depositor who loses yield)
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user1);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user2);

        // Deploy SplitMerge, grant MINTER_ROLE on YLD and SPLITTER_ROLE on registry
        splitMerge = new STBL_YLD_SplitMerge(address(registry));
        yld.grantRole(yld.MINTER_ROLE(), address(splitMerge));
        registry.grantRole(keccak256("SPLITTER_ROLE"), address(splitMerge));

        // Deploy the redemption contract (wrapped for state inspection)
        redemption = new InspectableRedemption4(
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

    /// @notice PoC: iDeposit() does not claim pending yield on the incoming NFT before merge burns it
    /// Title:    Missing yield claim on incoming NFT in iDeposit() — depositor's pending yield permanently trapped
    /// Affected: STBL_Redemption_Core.iDeposit() (lines 121-135)
    /// Impact:   When a depositor's NFT is merged into the pool, the merge burns the incoming NFT and
    ///           snapshots its pending distributor yield into stakingData[_id].earned. Because the NFT
    ///           no longer exists, distributor.claim(_id) permanently reverts. The depositor's accumulated
    ///           yield is irrecoverably trapped in dead storage — it can never be claimed by anyone.
    /// Author:   0xStalin
    function test_poc_depositorYieldLost() public {
        address distributor = getAssetYieldDistributor(ASSET_SLOT);
        address assetToken = getAssetToken(ASSET_SLOT);

        // == [ Phase 1: user1 deposits to establish a non-empty pool ] ==
        //
        // Required so the merge branch in iDeposit() is taken when user2 deposits.

        uint256 nft1 = _issueNFT(user1, DEPOSIT);

        vm.startPrank(user1);
        yld.approve(address(redemption), nft1);
        redemption.deposit(nft1);
        vm.stopPrank();

        uint256 poolNFTID = redemption.getNFTID();

        console.log("--- Phase 1: user1 establishes pool ---");
        console.log("user1 NFT ID deposited:", nft1);
        console.log("Pool NFTID after user1 deposit:", poolNFTID);
        console.log("Pool totalSupply:", redemption.getTotalSupply());

        // == [ Phase 2: user2's NFT is issued, then yield accrues for both NFTs ] ==
        //
        // user2 issues their NFT before any yield cycle so it is registered with the
        // YieldDistributor. Then time is advanced and yield is distributed — both the
        // pool NFT and user2's NFT accumulate pending yield in the distributor.
        // redemption.claimYield() is called to drain the pool NFT's pending yield into
        // the rewardIndex, isolating user2's NFT yield as the only remaining amount.

        uint256 user2_nft = _issueNFT(user2, DEPOSIT);

        console.log("--- Phase 2: yield accrues on user2 NFT ---");
        console.log("user2 NFT ID issued:", user2_nft);

        // Advance time past the yieldDuration lock so distributeYield() succeeds
        vm.warp(block.timestamp + 10_000_001);
        vm.roll(block.number + 1);

        vm.startPrank(admin);
        STBL_TestOracle(getAssetOracle(ASSET_SLOT)).setPrice();
        STBL_T1_Vault(getAssetVault(ASSET_SLOT)).distributeYield();
        vm.stopPrank();

        // Drain the pool NFT's pending yield to isolate user2's share
        redemption.claimYield();

        uint256 pendingYield = STBL_T1_YieldDistributor(distributor)
            .calculateRewardsEarned(user2_nft);

        console.log("Pool NFT pending yield (drained by claimYield):", redemption.getRewardIndex());
        console.log("user2 NFT pending yield in distributor (before deposit):", pendingYield);

        // Pre-condition: user2's NFT must have pending yield to demonstrate the loss
        assertGt(
            pendingYield,
            0,
            "pre-condition: user2 NFT must have pending yield before deposit"
        );

        // == [ Phase 3: user2 deposits — bug triggered ] ==
        //
        // Root cause path inside iDeposit():
        //   1. _updateRewards(user2) — snapshots user2's rewardIndex baseline
        //   2. YLD.transferFrom(user2, redemption, user2_nft)
        //   3. spliter.merge(NFTID, user2_nft) is called because NFTID != 0
        //      a. YLD.burn(user2_nft)  ← NFT no longer exists
        //      b. disableYield(user2_nft) ← snapshots pendingYield into
        //         stakingData[user2_nft].earned but the NFT is already burned
        //      c. distributor.claim(user2_nft) is now permanently impossible
        //         because ownerOf(user2_nft) reverts

        vm.startPrank(user2);
        yld.approve(address(redemption), user2_nft);
        redemption.deposit(user2_nft);
        vm.stopPrank();

        uint256 poolNFTID_after = redemption.getNFTID();

        console.log("--- Phase 3: user2 deposits (bug triggered) ---");
        console.log("user2 NFT ID merged (burned):", user2_nft);
        console.log("Pool NFTID before merge:", poolNFTID);
        console.log("Pool NFTID after merge (new merged NFT):", poolNFTID_after);
        console.log("Pool totalSupply after user2 deposit:", redemption.getTotalSupply());

        // The merge must have occurred — NFTID changed
        assertTrue(
            poolNFTID_after != poolNFTID,
            "post-deposit: pool NFTID must have changed (merge occurred)"
        );

        // == [ Phase 4: Verify impact — yield permanently trapped ] ==

        uint256 trappedYield = STBL_T1_YieldDistributor(distributor)
            .calculateRewardsEarned(user2_nft);

        (, , uint256 user2Earned) = redemption.getUserData(user2);
        // Simulate claim to get what user2 would actually receive from the pool
        uint256 user2BalBefore = STBL_TestToken(assetToken).balanceOf(user2);
        vm.prank(user2);
        uint256 user2Claimed = redemption.claim();
        uint256 user2BalAfter = STBL_TestToken(assetToken).balanceOf(user2);

        console.log("--- Phase 4: Verify impact ---");
        console.log("user2 pending yield before deposit:", pendingYield);
        console.log("Yield still trapped in burned NFT storage:", trappedYield);
        console.log("user2 earned in redemption pool (from pool rewardIndex):", user2Earned);
        console.log("user2 claimed from redemption pool:", user2Claimed);
        console.log("user2 token balance delta:", user2BalAfter - user2BalBefore);

        // Primary assertion: yield is permanently trapped in burned-NFT storage —
        // calculateRewardsEarned still returns the same amount as before the deposit.
        assertEq(
            trappedYield,
            pendingYield,
            "PoC: depositor yield permanently trapped in burned NFT storage"
        );

        // user2 received zero yield credit in the redemption pool
        assertEq(user2Claimed, 0, "PoC: depositor received zero yield from redemption pool");

        console.log("--- Phase 4b: Verify distributor.claim(user2_nft) reverts ---");

        // distributor.claim(user2_nft) must revert — NFT burned, ownerOf reverts
        vm.expectRevert();
        STBL_T1_YieldDistributor(distributor).claim(user2_nft);

        console.log("[+] EXPLOIT CONFIRMED: Depositor yield permanently trapped in burned NFT storage - user2 lost", trappedYield, "tokens of yield that can never be claimed");
    }
}
```

**Recommended Mitigation:** Before calling `merge`, claim any pending distributor yield for the incoming NFT `_id` on behalf of the depositor. The simplest form is to call the distributor's claim function for `_id` before the transfer and credit the proceeds to the depositor. If the protocol intends this to be a caller responsibility, it must be documented prominently and enforced via a check or revert when pending yield is detected.

**STBL:** Fixed in commit [2c09db6](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/2c09db65ae52fc1849dce5ed7193d2711f786b9e).

**Cyfrin:** Verified. `iDeposit` now calls `distributor.claim(_id)` on the incoming NFT before the transfer and merge, while the depositor still owns the NFT, ensuring any accrued yield flows directly to them rather than being trapped in burned-NFT storage.
