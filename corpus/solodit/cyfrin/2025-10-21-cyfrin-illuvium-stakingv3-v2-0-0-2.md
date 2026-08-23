---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Dust amounts of rewards get stuck in the Vault
vuln_class: []
---

# Dust amounts of rewards get stuck in the Vault

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** In `StakingVault`, rewards are distributed through the `notifyRewardAmount` function. However, due to the current implementation, some rewards can remain stuck in the contract because of rounding errors.

For example:

* User1 stakes `1e18`
* User2 stakes `7e18`
* The total reward amount is `1e18`

Because of rounding, the actual distributed reward will be less than `1e18`, specifically `999999999999000000`. This leaves a small portion of the reward undistributed and permanently stuck in the contract.

```solidity
function notifyRewardAmount(uint256 ilvAmount)
        external
        override
        nonReentrant
        whenNotPaused
        onlyRole(DISTRIBUTOR_ROLE)
    {
        // If no rewards are provided, return
        if (ilvAmount == 0) return;

        // Cache total staked for gas efficiency
        uint256 _totalStaked = totalStaked;

        // When no one is staking, return (prevents division by zero)
        if (_totalStaked == 0) {
            return;
        }

        // Update rewards-per-share accumulator
        accIlvPerShare += (ilvAmount * Constants.ACC_PRECISION) / _totalStaked;

        emit RewardsNotified(ilvAmount, accIlvPerShare);
    }
```

**Impact:** A portion of the reward tokens will remain stuck in the contract and will never be claimable by users, leading to inefficient distribution of rewards.

**Proof of Concept:** The following test demonstrates the issue and can be added to `StakingVault.t.sol`:

```solidity
function test_twoUsersWhoStakeAreEligibleForAllRewards() public {
    address user = makeAddr("User1");
    address user2 = makeAddr("User2");
    uint96 amount = 1e18;
    uint32 duration = 31 days;
    uint96 notifyAmt = 1e18;

    // User 1 and User 2 deposit
    approveAndDeposit(user, amount, duration);
    approveAndDeposit(user2, amount * 6, duration);

    // Fund and notify rewards
    ilv.mint(address(vault), notifyAmt);
    vm.prank(admin);
    vault.notifyRewardAmount(notifyAmt);

    // Check if total pending rewards equal notifyAmt
    uint256 pending = vault.pendingRewards(user);
    uint256 pending2 = vault.pendingRewards(user2);
    assertEq(pending + pending2, notifyAmt);
}
```

The assertion will fail because the total pending rewards do not equal the notified amount.

**Recommended Mitigation:** Increase the precision of the reward calculation by changing `ACC_PRECISION` from `1e12` to `1e18`.
This adjustment reduces the rounding error to at most **1 wei**, ensuring nearly all rewards are distributed correctly.

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
