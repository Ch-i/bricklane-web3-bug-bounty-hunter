---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Distributor can over-allocate claimables, causing temporary claim DoS
vuln_class: []
---

# Distributor can over-allocate claimables, causing temporary claim DoS

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** `L2RevenueDistributorV3::distribute` credits claimable pools by incrementing `pendingIlv` but does not reserve tokens for those future claims. Subsequent distributions that transfer ILV out to vaults can consume the same on-chain balance the claimables depend on. This can leave `sum(pendingIlv)` greater than the contract’s ILV balance, so a later `L2RevenueDistributorV3::claimPool` reverts until the distributor is topped up.

**Impact:** The system relies on ops keeping the distributor funded; if they don’t, claimable pools can be temporarily DoS’d  until a top-up. No permanent loss of funds, but availability is affected and accounting becomes misleading.

**Proof of Concept:** Add this test to `L2RevenueDistributorV3.t.sol`:
```solidity
    /// PoC: Overcommit claimables via two distributions -> claim reverts (insufficient balance)
    function test_PoC_Overcommit_BricksClaimables_TwoDistributes() public {
        // 1) Seed distributor
        uint256 amount1 = 1_000e18; // clean number to avoid rounding noise
        ilv.mint(address(distributor), amount1);

        // 2) First distribution. Pool 2 (claimable, 2000 bps) accrues 20% pending; 80% sent to vaults.
        vm.prank(operator);
        distributor.distribute(amount1);

        uint256 expectedPendingAfter1 = (amount1 * 2000) / Constants.BPS_DENOMINATOR;
        assertEq(pendingOf(2), expectedPendingAfter1, "pending after first distribute");
        assertEq(ilv.balanceOf(address(distributor)), expectedPendingAfter1, "residual ILV equals claimable pending");

        // 3) Naive second distribution using the entire remaining balance.
        uint256 amount2 = ilv.balanceOf(address(distributor)); // == expectedPendingAfter1
        vm.prank(operator);
        distributor.distribute(amount2);

        // Now: balance < pending (overcommitted)
        uint256 pendingNow = pendingOf(2); // 20% of amount1 + 20% of amount2
        uint256 balNow = ilv.balanceOf(address(distributor));
        assertLt(balNow, pendingNow, "distributor balance < claimable pending");

        vm.prank(admin);
        distributor.setClaimAllowlist(2, address(this), true);

        // 4) Claims are bricked until top-up
        vm.expectRevert("balance"); // SafeERC20 transfer fails due to insufficient ILV
        distributor.claimPool(2, address(this));
    }
```

**Recommended Mitigation:** Track what’s already promised to claimables and ensure distributions only spend the unreserved balance:

* Add a global accumulator:

  ```solidity
  uint256 public reservedClaimables;
  ```

* When allocating to a claimable pool, increase the reserve; when claiming, decrease it:

  ```solidity
  function _applyAllocation(Pool storage pool, uint256 amount) internal {
      if (pool.kind == PoolKind.Vault) {
          ilv.safeTransfer(pool.recipient, amount);
          IStakingVaultMinimal(pool.recipient).notifyRewardAmount(amount);
      } else {
          pool.pendingIlv += amount;
          reservedClaimables += amount;
      }
  }

  function claimPool(uint256 id, address to) external nonReentrant whenNotPaused {
      // ...existing checks...
      uint256 amount = pool.pendingIlv;
      if (amount == 0) revert NothingToClaim(id);
      pool.pendingIlv = 0;
      reservedClaimables -= amount;     // reduce reserved on successful claim
      ilv.safeTransfer(to, amount);
      emit PoolClaimed(id, to, amount);
  }
  ```

* Before performing a distribution, ensure the request does not exceed the unreserved ILV on the contract:

  ```solidity
  error InsufficientUnreservedBalance();

  function distribute(uint256 ilvAmount) external nonReentrant whenNotPaused onlyRole(OPERATOR_ROLE) {
      if (ilvAmount == 0) revert DistributeAmountZero();

      if (ilvAmount > ilv.balanceOf(address(this) - reservedClaimables) revert InsufficientUnreservedBalance();

      // proceed with existing allocation logic...
  }
  ```

This enforces `balance - claimable >= amount` at the start of `distribute()`, guaranteeing that claimable promises are always backed by on-contract tokens and preventing overcommit/DoS of `claimPool()`.


**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
