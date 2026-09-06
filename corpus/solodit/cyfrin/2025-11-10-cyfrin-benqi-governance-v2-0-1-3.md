---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Votes will continue to be automatically recast for deactivated gauges if prior
  voters do not reset
vuln_class: []
---

# Votes will continue to be automatically recast for deactivated gauges if prior voters do not reset

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The `test_calculateSpeeds_positiveVotesNoGauge()` function in `BenqiCoreModule.calculateSpeeds.t.sol` contains the assumption that such a scenario in which a non-existent gauge has non-zero votes should not happen in practice:

```solidity
function test_calculateSpeeds_positiveVotesNoGauge() public view {
    // This shouldn't happen in practice, but testing edge case
    IBenqiCoreState.MarketVotes memory market = IBenqiCoreState.MarketVotes({
        qiToken: QITOKEN_1,
        supplyVotes: 100, // Has votes but no gauge
        borrowVotes: 200,
        hasRegisteredSupplyGauge: false,
        hasRegisteredBorrowGauge: false
    });

    uint256 currentSupplySpeed = 5000;
    uint256 currentBorrowSpeed = 6000;

    (uint256 supplySpeed, uint256 borrowSpeed) = module.calculateSpeeds(
        market,
        1000, // totalVotes
        MODULE_BUDGET,
        EPOCH_DURATION,
        currentSupplySpeed,
        currentBorrowSpeed
    );

    // No gauges, should preserve current speeds despite votes
    assertEq(supplySpeed, currentSupplySpeed);
    assertEq(borrowSpeed, currentBorrowSpeed);
}
```

However, this is not strictly true and can occur for deactivated gauges because votes are automatically recast in the absence of a reset when previous voters vote for other gauges. This could result in an unregistered/deactivated gauge having phantom voting power, for example if the gauge is deactivated directly on the `AddressGaugeVoter` without also being unregistered from the `GaugeRegistrar` since the gauges for the controller are retrieved from the `GaugeRegistrar`, meaning this deactivation this won’t be reflected. The auto-recast votes will not be reset, so any controller that has its gauge deactivated in this manner will continue to receive a share of rewards.

**Impact:** Distributions are unaffected by gauge deactivations in `AddressGaugeVoter`.

**Proof of Concept:** The following test should be added to `BenqiIntegrationSingleEpoch.t.sol`:

```solidity
function test_votesRecastAndRewardsDistributedToDeactivatedGauge() public {
    if (!useFork) return;

    // Setup budget for multiple epochs
    {
        uint budget = allocator.totalQiBudget();
        uint totalNeeded = (budget + ((budget * BUFFER) / 10_000)) * 2; // For 2 epochs
        mintOrSend(address(dao), totalNeeded, useFork);
    }

    // Ensure we're not in a voting window before registering gauges
    vm.warp(clock.epochVoteEndTs() + 1);
    assertFalse(voter.votingActive(), "Should not be voting active");

    address gEcoSupply;
    address gCoreBorrow;
    vm.startPrank(address(dao));
    {
        gEcoSupply = registrar.registerGauge(
            address(qiTokenM0),
            IGaugeRegistrar.Incentive.Supply,
            address(distributor),
            "USDC Ecosystem Supply Gauge"
        );

        gCoreBorrow = registrar.registerGauge(
            address(qiTokenC0),
            IGaugeRegistrar.Incentive.Borrow,
            address(coreComptroller),
            "USDC Core Borrow Gauge"
        );
    }
    vm.stopPrank();

    // define a user
    address guy = address(0x1337);

    // mint them tokens
    mintOrSend(guy, 1000e18, useFork);

    // stake the tokens
    uint tokenId1;
    uint tokenId2;
    vm.startPrank(guy);
    {
        miles.approve(address(escrow), 1000e18);
        tokenId1 = escrow.createLock(990e18);
        tokenId2 = escrow.createLock(10e18);
        adapter.delegate(guy);
        assertEq(adapter.getVotes(guy), 1000e18, "votes");
    }
    vm.stopPrank();

    // go to voting window
    vm.warp(clock.epochVoteStartTs());
    assertTrue(voter.votingActive(), "V!A");

    // vote - 50/50 split between ecosystem and core
    GaugeVote[] memory votes = new GaugeVote[](2);
    votes[0] = GaugeVote({gauge: gEcoSupply, weight: 10000});
    votes[1] = GaugeVote({gauge: gCoreBorrow, weight: 10000});

    assertEq(adapter.getVotes(guy), 1000e18, "votes");

    vm.prank(guy);
    voter.vote(votes);

    assertEq(voter.epochGaugeVotes(0, gEcoSupply), 500e18, "eco gauge votes");
    assertEq(voter.epochGaugeVotes(0, gCoreBorrow), 500e18, "core gauge votes");

    // go to dist window
    vm.warp(clock.epochNextCheckpointTs());
    assertFalse(voter.votingActive(), "VA");

    // Capture state before distribution
    DualDistributionState memory state;
    {
        state.currentEpochId = clock.currentEpoch();
        state.initialDaoBalance = miles.balanceOf(address(dao));
        state.initialDistributorBalance = miles.balanceOf(address(distributor));
        state.initialCoreBalance = miles.balanceOf(address(coreComptroller));

        // Capture previous epoch distribution status
        if (state.currentEpochId > 0) {
            state.prevEpochDistributed = dmgr.isDistributed(state.currentEpochId - 1);
        }

        // Ecosystem state
        state.ecoConfigBefore = distributor.getConfigForMarket(qiTokenM0, address(miles));

        // Core state
        state.coreSupplySpeedBefore = coreComptroller.supplyRewardSpeeds(0, address(qiTokenC0));
        state.coreBorrowSpeedBefore = coreComptroller.borrowRewardSpeeds(0, address(qiTokenC0));

        // Calculate expected values
        state.totalBudget = allocator.totalQiBudget();
        // Since we have 2 controllers and votes are split 50/50
        // First allocator splits budget between controllers based on total votes
        // In this case, each controller gets 50% of total budget
        state.ecosystemBudget = state.totalBudget / 2;
        state.coreBudget = state.totalBudget / 2;

        // Each gauge gets 100% of its controller's budget (since only one gauge per controller)
        state.expectedEcoSpeed = state.ecosystemBudget / clock.epochDuration();
        state.expectedCoreSpeed = state.coreBudget / clock.epochDuration();

        // Calculate actual transfers based on budgetUsed (speed * epochDuration)
        // This accounts for rounding in integer division
        uint256 ecoBudgetUsed = state.expectedEcoSpeed * clock.epochDuration();
        uint256 coreBudgetUsed = state.expectedCoreSpeed * clock.epochDuration();

        // DistributionManager transfers budgetUsed + buffer, NOT allocatedBudget + buffer
        state.expectedEcoTransfer = ecoBudgetUsed + ((ecoBudgetUsed * BUFFER) / 10_000);
        state.expectedCoreTransfer = coreBudgetUsed + ((coreBudgetUsed * BUFFER) / 10_000);
        state.expectedTotalTransfer = state.expectedEcoTransfer + state.expectedCoreTransfer;
    }

    // distribute
    vm.prank(address(dao));
    dmgr.distribute();

    // Capture post-distribution state
    {
        state.ecoConfigAfter = distributor.getConfigForMarket(qiTokenM0, address(miles));
        state.coreSupplySpeedAfter = coreComptroller.supplyRewardSpeeds(0, address(qiTokenC0));
        state.coreBorrowSpeedAfter = coreComptroller.borrowRewardSpeeds(0, address(qiTokenC0));
    }

    // Run core assertions
    {
        // 1. Distribution marked for current epoch only
        assertTrue(
            dmgr.isDistributed(state.currentEpochId),
            "Current epoch should be marked as distributed"
        );

        // Verify previous epoch status unchanged (if exists)
        if (state.currentEpochId > 0) {
            assertEq(
                dmgr.isDistributed(state.currentEpochId - 1),
                state.prevEpochDistributed,
                "Previous epoch distribution status should remain unchanged"
            );
        }

        // Verify next epoch is NOT distributed
        assertFalse(
            dmgr.isDistributed(state.currentEpochId + 1),
            "Next epoch should not be distributed"
        );

        // 2. Token balances updated
        assertEq(
            miles.balanceOf(address(dao)),
            state.initialDaoBalance - state.expectedTotalTransfer,
            "DAO balance should decrease by total actual transfer"
        );

        assertEq(
            miles.balanceOf(address(distributor)),
            state.initialDistributorBalance + state.expectedEcoTransfer,
            "Distributor should receive ecosystem transfer"
        );

        assertEq(
            miles.balanceOf(address(coreComptroller)),
            state.initialCoreBalance + state.expectedCoreTransfer,
            "Core comptroller should receive core transfer"
        );

        // 3. Ecosystem market speeds updated
        assertEq(
            state.ecoConfigAfter.supplyEmissionsPerSec,
            state.expectedEcoSpeed,
            "Ecosystem supply speed should match expected"
        );
        assertEq(
            state.ecoConfigAfter.borrowEmissionsPerSec,
            state.ecoConfigBefore.borrowEmissionsPerSec,
            "Ecosystem borrow speed should remain unchanged (supply gauge only)"
        );

        // 4. Core market speeds updated
        assertEq(
            state.coreSupplySpeedAfter,
            state.coreSupplySpeedBefore,
            "Core supply speed should remain unchanged (borrow gauge only)"
        );
        assertEq(
            state.coreBorrowSpeedAfter,
            state.expectedCoreSpeed,
            "Core borrow speed should match expected"
        );
    }

    // Deactivate gEcoSupply
    vm.prank(address(dao));
    voter.deactivateGauge(gEcoSupply);

    // go to voting window
    vm.warp(clock.epochVoteStartTs());
    assertTrue(voter.votingActive(), "V!A");

    // Votes are automatically recast
    assertEq(voter.epochGaugeVotes(0, gEcoSupply), 500e18, "eco gauge votes");
    assertEq(voter.epochGaugeVotes(0, gCoreBorrow), 500e18, "core gauge votes");

    // go to dist window
    vm.warp(clock.epochNextCheckpointTs());
    assertFalse(voter.votingActive(), "VA");

    // Capture state before distribution
    {
        state.currentEpochId = clock.currentEpoch();
        state.initialDaoBalance = miles.balanceOf(address(dao));
        state.initialDistributorBalance = miles.balanceOf(address(distributor));
        state.initialCoreBalance = miles.balanceOf(address(coreComptroller));

        // Capture previous epoch distribution status
        if (state.currentEpochId > 0) {
            state.prevEpochDistributed = dmgr.isDistributed(state.currentEpochId - 1);
        }

        // Ecosystem state
        state.ecoConfigBefore = distributor.getConfigForMarket(qiTokenM0, address(miles));

        // Core state
        state.coreSupplySpeedBefore = coreComptroller.supplyRewardSpeeds(0, address(qiTokenC0));
        state.coreBorrowSpeedBefore = coreComptroller.borrowRewardSpeeds(0, address(qiTokenC0));

        // Calculate expected values
        state.totalBudget = allocator.totalQiBudget();
        // Since we have 2 controllers and votes are split 50/50
        // First allocator splits budget between controllers based on total votes
        // In this case, each controller gets 50% of total budget
        state.ecosystemBudget = state.totalBudget / 2;
        state.coreBudget = state.totalBudget / 2;

        // Each gauge gets 100% of its controller's budget (since only one gauge per controller)
        state.expectedEcoSpeed = state.ecosystemBudget / clock.epochDuration();
        state.expectedCoreSpeed = state.coreBudget / clock.epochDuration();

        // Calculate actual transfers based on budgetUsed (speed * epochDuration)
        // This accounts for rounding in integer division
        uint256 ecoBudgetUsed = state.expectedEcoSpeed * clock.epochDuration();
        uint256 coreBudgetUsed = state.expectedCoreSpeed * clock.epochDuration();

        // DistributionManager transfers budgetUsed + buffer, NOT allocatedBudget + buffer
        state.expectedEcoTransfer = ecoBudgetUsed + ((ecoBudgetUsed * BUFFER) / 10_000);
        state.expectedCoreTransfer = coreBudgetUsed + ((coreBudgetUsed * BUFFER) / 10_000);
        state.expectedTotalTransfer = state.expectedEcoTransfer + state.expectedCoreTransfer;
    }

    // distribute
    vm.prank(address(dao));
    dmgr.distribute();

    // Capture post-distribution state
    {
        state.ecoConfigAfter = distributor.getConfigForMarket(qiTokenM0, address(miles));
        state.coreSupplySpeedAfter = coreComptroller.supplyRewardSpeeds(0, address(qiTokenC0));
        state.coreBorrowSpeedAfter = coreComptroller.borrowRewardSpeeds(0, address(qiTokenC0));
    }

    // Run core assertions
    {
        // 1. Distribution marked for current epoch only
        assertTrue(
            dmgr.isDistributed(state.currentEpochId),
            "Current epoch should be marked as distributed"
        );

        // Verify previous epoch status unchanged (if exists)
        if (state.currentEpochId > 0) {
            assertEq(
                dmgr.isDistributed(state.currentEpochId - 1),
                state.prevEpochDistributed,
                "Previous epoch distribution status should remain unchanged"
            );
        }

        // Verify next epoch is NOT distributed
        assertFalse(
            dmgr.isDistributed(state.currentEpochId + 1),
            "Next epoch should not be distributed"
        );

        // 2. Token balances updated
        assertEq(
            miles.balanceOf(address(dao)),
            state.initialDaoBalance - state.expectedTotalTransfer,
            "DAO balance should decrease by total actual transfer"
        );

        assertEq(
            miles.balanceOf(address(distributor)),
            state.initialDistributorBalance + state.expectedEcoTransfer,
            "Distributor should receive ecosystem transfer"
        );

        assertEq(
            miles.balanceOf(address(coreComptroller)),
            state.initialCoreBalance + state.expectedCoreTransfer,
            "Core comptroller should receive core transfer"
        );

        // 3. Ecosystem market speeds updated
        assertEq(
            state.ecoConfigAfter.supplyEmissionsPerSec,
            state.expectedEcoSpeed,
            "Ecosystem supply speed should match expected"
        );
        assertEq(
            state.ecoConfigAfter.borrowEmissionsPerSec,
            state.ecoConfigBefore.borrowEmissionsPerSec,
            "Ecosystem borrow speed should remain unchanged (supply gauge only)"
        );

        // 4. Core market speeds updated
        assertEq(
            state.coreSupplySpeedAfter,
            state.coreSupplySpeedBefore,
            "Core supply speed should remain unchanged (borrow gauge only)"
        );
        assertEq(
            state.coreBorrowSpeedAfter,
            state.expectedCoreSpeed,
            "Core borrow speed should match expected"
        );
    }

    console2.log("voter.isActive(gEcoSupply): %s", voter.isActive(gEcoSupply));
    console2.log("Ecosystem continues to receive rewards despite the gauge being deactivated");
}
```

**Recommended Mitigation:** Consider preventing gauges from being deactivated on the voter without also notifying the registrar.

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.
