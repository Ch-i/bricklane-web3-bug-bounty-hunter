---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-14
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Accumulative reward setting to prevent overwrite and support incremental updates
vuln_class: []
---

# Accumulative reward setting to prevent overwrite and support incremental updates

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `Rewards::setRewardsAmountForEpochs` function allows an authorized distributor to set a fixed reward amount for a specific number of future epochs. This is typically called to define reward schedules—for example, assigning 20 tokens per epoch from epoch 1 to 5.

However, the current implementation **does not check whether rewards have already been set** for the target epochs. As a result, calling this function again for the same epochs **silently overrides the existing rewards**, leading to unintended consequences:

1. **Previously allocated rewards are overwritten.**
2. **New rewards are written to storage, but tokens from the previous call remain locked in the contract**, as there is no mechanism to refund or reallocate them.

Assume the following:

1. Distributor calls `setRewardsAmountForEpochs(1, 1, USDC, 100)`
   → Epoch 1 is allocated 100 USDC
   → 100 USDC is transferred into the contract

2. Later, a second call is made:
   `setRewardsAmountForEpochs(1, 1, USDC, 50)`
   → Epoch 1 is now reallocated to 50 USDC
   → **Original 100 USDC still sits in the contract**, but only 50 will be distributed
   → The difference (100 USDC) becomes stuck

**Impact:** **Loss of Funds:** Overwritten rewards are effectively stranded in the contract with no mechanism to recover or redistribute them.
**Unexpected Behavior for Distributors:** Calling `setRewardsAmountForEpochs` twice for the same epoch silently overrides the original intent without warning.

**Proof of Concept:** Add this test to `Rewards`:

```solidity
function test_setRewardsAmountForEpochs() public {
        uint256 rewardsAmount = 1_000_000 * 10 ** 18;
        ERC20Mock rewardsToken1 = new ERC20Mock();
        rewardsToken1.mint(REWARDS_DISTRIBUTOR_ROLE, 2 * 1_000_000 * 10 ** 18);
        vm.prank(REWARDS_DISTRIBUTOR_ROLE);
        rewardsToken1.approve(address(rewards), 2 * 1_000_000 * 10 ** 18);
        vm.prank(REWARDS_DISTRIBUTOR_ROLE);
        rewards.setRewardsAmountForEpochs(5, 1, address(rewardsToken1), rewardsAmount);
        assertEq(rewards.getRewardsAmountPerTokenFromEpoch(5, address(rewardsToken1)), rewardsAmount - Math.mulDiv(rewardsAmount, 1000, 10000));
        assertEq(rewardsToken1.balanceOf(address(rewards)), rewardsAmount);
        vm.prank(REWARDS_DISTRIBUTOR_ROLE);
        rewards.setRewardsAmountForEpochs(5, 1, address(rewardsToken1), rewardsAmount);
        assertEq(rewardsToken1.balanceOf(address(rewards)), rewardsAmount * 2 );

        assertEq(rewards.getRewardsAmountPerTokenFromEpoch(5, address(rewardsToken1)), (rewardsAmount - Math.mulDiv(rewardsAmount, 1000, 10000)) * 2);
    }
```

 **Recommended Mitigation:**

Add a **guard clause** in the `setRewardsAmountForEpochs` function to **prevent overwriting rewards** for epochs that already have a value set:

```diff
for (uint48 i = 0; i < numberOfEpochs; i++) {

-    rewardsAmountPerTokenFromEpoch[startEpoch + i].set(rewardsToken, rewardsAmount);
+    uint256 existingAmount = rewardsAmountPerTokenFromEpoch[targetEpoch].get(rewardsToken);
+   rewardsAmountPerTokenFromEpoch[targetEpoch].set(rewardsToken, existingAmount + rewardsAmount);
}
```

**Suzaku:**
Fixed in commit [a5c4913](https://github.com/suzaku-network/suzaku-core/pull/155/commits/a5c4913f9f73aa9f87e0026f4fac1cade95b8e64).

**Cyfrin:** Verified.
