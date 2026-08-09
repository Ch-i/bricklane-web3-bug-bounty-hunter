---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Reward distribution can be skipped when executed within the vote window buffer
  of a new epoch
vuln_class: []
---

# Reward distribution can be skipped when executed within the vote window buffer of a new epoch

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** `DistributionManager::distribute` is validated to only be callable when voting is not active. This is achieved by calling `_validateCanDistribute()`; however, this fails to account for the `VOTE_WINDOW_BUFFER` period at the start of each epoch.

The Clock contract defines epochs with the following structure:

* `EPOCH_DURATION`: 2 weeks
* `VOTE_DURATION`: 1 week
* `VOTE_WINDOW_BUFFER`: 1 hour

```solidity
    function _validateCanDistribute(IClock _clock) internal view {
        if (_activeRewardControllers.length() == 0) revert NoModulesConfigured();
@>      if (_clock.votingActive()) revert VotingStillActive(); // @audit - returns false in buffer period

@>      uint256 currentEpochId = _clock.currentEpoch(); // @audit - returns N+1
@>      if (_isEpochDistributed(currentEpochId)) { // @audit - checks if N+1 distributed, not N
            revert EpochAlreadyDistributed(currentEpochId);
        }
    }
```

For each epoch, voting is only active from `T = 1 hour` to `T = 1 week - 1 hour`; however, when a new epoch begins, there's a 1-hour buffer period where:

* `votingActive()` returns false
* `currentEpoch()` returns the new epoch N+1

This incorrectly allows for distributions to occur in the first hour of the epoch N+1, preventing subsequent distribution for the epoch.

**Impact:** If `distribute()` is called during the 1-hour window at the start of epoch N+1, for example in the case of late distribution of epoch N, both epochs N and N+1 will never be distributed. The system will mark epoch N+1 as distributed before any votes have been cast for it.

**Proof of Concept:** The following test should be added to `DistributorManager.distribute.t.sol`:

```solidity
 function testPoC_bufferWindowSkipsEpoch() public {
    // Setup gauge and votes for epoch 0
    vm.prank(ADMIN);
    address gauge = gaugeRegistrar.registerGauge(
        QI_TOKEN_1, IGaugeRegistrar.Incentive.Supply, address(coreComptroller), "Gauge"
    );
    coreComptroller.setMarketListed(QI_TOKEN_1, true);
    addressGaugeVoter.setEpochGaugeVotes(0, gauge, 1000 ether);

    // Warp to 30 minutes into epoch 1 (in VOTE_WINDOW_BUFFER)
    vm.warp(2 weeks + 30 minutes);

    // Verify preconditions: epoch 1, voting inactive, in buffer period
    assertEq(clock.currentEpoch(), 1);
    assertFalse(clock.votingActive());
    assertLt(clock.elapsedInEpoch(), 1 hours);

    // Call distribute() - should fail but doesn't
    vm.prank(DISTRIBUTOR);
    distributionManager.distribute();

    // BUG: Epoch 1 marked distributed, Epoch 0 skipped forever
    assertFalse(distributionManager.isDistributed(0), "Epoch 0 never distributed!");
    assertTrue(distributionManager.isDistributed(1), "Epoch 1 wrongly marked distributed");
}
```

As described, the epoch 0 rewards were never distributed and the epoch 1 was distributed with 0 votes and zero budget.

**Recommended Mitigation:** Either explicitly prevent distribution during the vote window buffer or, preferably, allow distribution for the previous epoch within this period.

**BENQI:** Fixed in commit PR [\#13](https://github.com/aragon/benqi-governance/pull/13).

**Cyfrin:** Verified. Distributions can no longer be made during the pre-vote buffer period.
