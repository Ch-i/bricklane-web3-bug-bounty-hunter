---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: Wrong `USST` approval target in `STBL_ESS_Wrapper1::asset_Withdraw` leaves
  standing USST allowance on issuer
vuln_class: []
---

# Wrong `USST` approval target in `STBL_ESS_Wrapper1::asset_Withdraw` leaves standing USST allowance on issuer

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_ESS_Wrapper1` is the abstract base contract implementing the ESS withdrawal flow. Its internal `asset_Withdraw` function iterates over the YLD NFTs in a vault lot and for each NFT calls `approve` before invoking `iSTBL_Issuer::withdraw`:

```solidity
STBL_USST.approve(Ratios[MetaData.assetID].issuer, MetaData.stableValueNet);
iSTBL_Issuer(Ratios[MetaData.assetID].issuer).withdraw(nftIDs[i]);
```

The approval targets the issuer contract. However, the issuer's `withdraw` call chains internally to `STBL_Core::exit`, which calls `USST::burn`. The USST `burn` implementation is:

```solidity
IERC20(address(this)).safeTransferFrom(_from, address(this), _amt);
```

The spender is `address(this)` — the USST contract itself. The required allowance is `allowance[wrapper][USST_contract]`; the issuer is never the spender and never uses the allowance set by the abstract.

The concrete `STBL_XLayer_Wrapper` compensates at initialization with `IERC20(usstToken).approve(usstToken, type(uint256).max)`, so the current deployment is not broken.

The risk is latent: any future concrete implementation that extends `STBL_ESS_Wrapper1` without replicating this initialization-time approval will have all `ess_withdraw` calls revert at the USST burn step, permanently locking ESS holders out of their underlying assets.


A secondary consequence is a persistent standing allowance. Because ERC-20 `approve` sets (not increments) the allowance, after each `asset_Withdraw` loop the issuer is left with `allowance[wrapper][issuer] = stableValueNet_of_last_NFT` — unspent and never revoked.

**Proof of Concept:**
- `test_poc_wrongApprovalTarget_StandingAllowance` — completes a successful withdrawal and asserts both issuers hold non-zero USST allowances (`issuer1: 2,908.8 USST`, `issuer2: 6,787.2 USST`) that were never consumed.
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./XLayer_Setup.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title XLayer_Withdraw_PoC
 * @notice Proof-of-concept for the wrong USST approval target in STBL_ESS_Wrapper1.asset_Withdraw.
 *
 * Root cause: asset_Withdraw (STBL_ESS_Wrapper1.sol:215-218) calls
 *   STBL_USST.approve(Ratios[MetaData.assetID].issuer, MetaData.stableValueNet)
 * but the actual USST burn in STBL_Core.exit() calls
 *   USST.burn(wrapper, value) -> safeTransferFrom(wrapper, USST, amt)
 * meaning the spender must be the USST contract itself, not the issuer.
 *
 * The current deployment is only functional because STBL_XLayer_Wrapper.initialize sets
 *   IERC20(usstToken).approve(usstToken, type(uint256).max)
 * which is the compensating max approval. Without it, every ess_withdraw reverts.
 *
 * Two impacts are demonstrated below:
 *   (1) DoS when the compensating max approval is absent.
 *   (2) Issuer accumulates a standing, unspent USST allowance after every successful withdrawal.
 */
contract XLayer_Withdraw_PoC is XLayer_Setup {
    uint256 constant DEPOSIT_AMOUNT = 9696 * 10 ** 18;

    function setUp() public override {
        super.setUp();
        mintTestTokensToUser(user1, 100_000 * 10 ** 18);
        approveWrapperForUser(user1);
    }

    // == [ PoC : Standing issuer allowance — issuer retains unspent USST allowance after withdrawal ] ==

    /// @notice PoC: Wrong USST approval target in asset_Withdraw
    /// Title:    Wrong USST approval target in asset_Withdraw breaks ESS withdrawals and leaves standing USST allowance on issuer
    /// Affected: STBL_ESS_Wrapper1.sol:214-221
    /// Impact:   (1) ESS withdrawals DoS in any deployment without compensating init-time max approval; (2) issuer accumulates unspent USST allowance on every withdrawal
    /// Author:   0xStalin
    function test_poc_wrongApprovalTarget_StandingAllowance() public {
        // == [ Step 1: User deposits to receive ESS tokens and a lot ] ==
        vm.startPrank(user1);
        uint256 lotId = xLayerWrapper.ess_deposit(DEPOSIT_AMOUNT);
        vm.stopPrank();

        uint256 essReceived = xLayerToken.balanceOf(user1);

        console.log("=== PoC 2: Standing issuer USST allowance after withdrawal ===");
        console.log("[*] Deposit complete. lotId:", lotId);
        console.log("[*] ESS tokens received:", essReceived / 1e18);

        // == [ Step 2: Confirm issuers hold zero USST allowance before withdrawal ] ==
        uint256 issuer1AllowanceBefore = usst.allowance(
            address(xLayerWrapper),
            address(issuer1)
        );
        uint256 issuer2AllowanceBefore = usst.allowance(
            address(xLayerWrapper),
            address(issuer2)
        );
        console.log("[*] issuer1 USST allowance before withdrawal:", issuer1AllowanceBefore);
        console.log("[*] issuer2 USST allowance before withdrawal:", issuer2AllowanceBefore);

        // == [ Step 3: Approve wrapper to spend the user's ESS tokens, then withdraw ] ==
        // _Wrapper_ess_withdraw pulls ESS from caller via transferFrom.
        vm.startPrank(user1);
        xLayerToken.approve(address(xLayerWrapper), type(uint256).max);

        // Warp time to satisfy PT duration requirement (assets configured with 7-day duration)
        vm.warp(block.timestamp + 8 days);

        uint256[] memory nftIds = xLayerWrapper.ess_withdraw(lotId);
        vm.stopPrank();

        console.log("[*] ess_withdraw succeeded. NFTs redeemed:", nftIds.length);

        // == [ Step 4: Assert that the issuers now hold unspent USST allowances ] ==
        uint256 issuer1AllowanceAfter = usst.allowance(
            address(xLayerWrapper),
            address(issuer1)
        );
        uint256 issuer2AllowanceAfter = usst.allowance(
            address(xLayerWrapper),
            address(issuer2)
        );

        console.log("[*] issuer1 USST allowance after withdrawal:", issuer1AllowanceAfter);
        console.log("[*] issuer2 USST allowance after withdrawal:", issuer2AllowanceAfter);

        // The issuers were never the correct spender — they never consumed the allowance.
        // Both should be non-zero, demonstrating the standing capability granted unnecessarily.
        assertGt(
            issuer1AllowanceAfter,
            0,
            "issuer1 must hold unspent USST allowance (standing capability)"
        );
        assertGt(
            issuer2AllowanceAfter,
            0,
            "issuer2 must hold unspent USST allowance (standing capability)"
        );

        console.log("[+] CONFIRMED: issuers hold unspent USST allowances after successful withdrawal");
        console.log("[+] issuer1 standing USST allowance:", issuer1AllowanceAfter);
        console.log("[+] issuer2 standing USST allowance:", issuer2AllowanceAfter);
    }
}
```

**Recommended Mitigation:** In `STBL_ESS_Wrapper1::asset_Withdraw`, replace the approval target from the issuer address to `address(STBL_USST)` to align with the USST burn mechanism:

This makes the abstract self-consistent, eliminates the issuer's standing allowance, and removes the dependency on concrete implementations to compensate via an initialization-time max approval.


**STBL:** Fixed in commits [cb5f79e](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/cb5f79ebcb122d1f58e5a69a8784a5594765227c) & [41002d1](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/41002d1eb06663ac0792db2b15ef851602f426d4).

**Cyfrin:** Verified. The approval target in `asset_Withdraw` was corrected from the `issuer` address to the `USST` token contract itself, aligning with how the `USST` burn mechanism works.
