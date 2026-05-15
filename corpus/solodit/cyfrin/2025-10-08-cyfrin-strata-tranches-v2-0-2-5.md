---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-2-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: '`Tranche::maxMint` for Junior Tranches is at risk of overflow when the `jrNav`
  falls below `1:1` rate to `JR_Shares`'
vuln_class: []
---

# `Tranche::maxMint` for Junior Tranches is at risk of overflow when the `jrNav` falls below `1:1` rate to `JR_Shares`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** Given that the system is composed of two tranches (Senior and Junior), and all the assets deposited among the two Tranches are polled together on the Strategy, the actual `totalAssets()` for each Tranche is calculated using the corresponding NAVs (`srtNav` and `jrtNav`).
The Junior Tranche has the peculiarity that can be used to:
1. Fund the Senior's target APR when the generated APR is not enough.
2. Cover losses by taking the hit first and covering as much as possible to limit/reduce the loss for the Seniors.

Any of the above two events results in a decrease in the `jrtNav`, which is translated into the `totalAssets()` for the Junior Tranche being decremented. As a result, the JR Shares to assets decrements and can cause the `share<=>assets` rate to fall below 1:1.

When the `JR_Shares<=>assets` falls below 1:1, `maxMint()` results in overflow because the underlying Math methods implemented for the conversions of shares to assets, and the fact that `assets` to be converted is set as `type(uint256).max`

**Impact:** DoS of `Tranche::mint` because `Tranche::maxMint` reverts due to an overflow when converting shares to assets.

**Proof of Concept:** As demonstrated on the next PoC, when the JR_Shares<=>assets rate falls below 1:1, any calls to `Tranche::maxMint` result in overflow, effectively reverting the tx.

Add the following PoC to `CDO.t.sol` test file:
```solidity
    function test_MaxMintOverflowsInJrTranche() public {
        address alice = makeAddr("Alice");

        uint256 initialDeposit = 1000 ether;
        USDe.mint(alice, initialDeposit);

        vm.startPrank(alice);
        USDe.approve(address(jrtVault), type(uint256).max);
        jrtVault.deposit(initialDeposit, alice);
        vm.stopPrank();

//@audit-info => Simulate 10% losses on the Jr Strategy
//@audit => This would be akin to JR Tranche covering losses or making Senior's APR whole.
        vm.prank(address(sUSDeStrategy));
        sUSDe.transfer(alice, initialDeposit / 10);

        vm.expectRevert();
        jrtVault.maxMint(alice);
    }
```

**Recommended Mitigation:** Given that the max deposits for the Jr Tranche are unlimited, it's okay to return an unlimited max shares too.
- Skip the convertion of assets to shares when `CDO::maxDeposit` returns `type(uint256).max` and instead return the same value.

```diff
// Tranche::maxMint //

    function maxMint(address owner) public view override returns (uint256) {
        uint256 assets = cdo.maxDeposit(address(this));
+       if (assets == type(uint256).max) {
+          return type(uint256).max;
+       }
        return convertToShares(assets);
    }


```

**Strata:**
Fixed in commit [5748b2f](https://github.com/Strata-Money/contracts-tranches/commit/5748b2f292ae3f56335361633d77c9bb30e4d7fa) by not converting `type(uint256).max` onto shares and instead returning that value as max shares to mint for JR Tranche.

**Cyfrin:** Verified.

\clearpage
