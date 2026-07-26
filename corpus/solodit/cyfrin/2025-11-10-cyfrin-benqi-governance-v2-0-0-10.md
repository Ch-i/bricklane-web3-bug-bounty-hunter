---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-10
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Arbitrary controller addresses can be passed to `DistributionManager::setModuleForController`
  without validation of the corresponding gauge addresses
vuln_class: []
---

# Arbitrary controller addresses can be passed to `DistributionManager::setModuleForController` without validation of the corresponding gauge addresses

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The DAO can currently pass any arbitrary controller address in calls to `DistributionManager::setModuleForController`; however, this logic should additionally validate that the gauges of the controller are registered on the `GaugeRegistrar` and `AddressGaugeVoter` to avoid adding an invalid controller to the `_activeRewardControllers` set:

```solidity
/// @dev Internal function to set module for controller
function _setModuleForController(
    address _rewardController,
    IDistributionModule _module
) internal {
    if (_rewardController == address(0)) revert InvalidAddress("rewardController");
    if (address(_module) == address(0)) revert InvalidAddress("module");

    // Enforce one module per controller constraint
    if (address(rewardControllerToModule[_rewardController]) != address(0)) {
        revert ControllerAlreadyRegistered(_rewardController);
    }

@>  _activeRewardControllers.add(_rewardController);

    rewardControllerToModule[_rewardController] = _module;

    emit ModuleForControllerSet(_rewardController, address(_module));
}
```

Impact is low since the DAO is unlikely to deliberately configure this incorrectly. Nevertheless, `_validateCanDistribute()` can return true in this scenario since it only checks the length of active reward controllers is non-zero rather than the gauges corresponding to those controllers:

```solidity
    function _validateCanDistribute(IClock _clock) internal view {
@>      if (_activeRewardControllers.length() == 0) revert NoModulesConfigured();
        if (_clock.votingActive()) revert VotingStillActive();

        uint256 currentEpochId = _clock.currentEpoch();
        if (_isEpochDistributed(currentEpochId)) {
            revert EpochAlreadyDistributed(currentEpochId);
        }
    }
```

Given that within `_collectVotes()` the gauge addresses are attempted to be queried from the `GaugeRegistrar`, an empty array will always be returned for invalid controller addresses:

```solidity
address controller = _activeRewardControllers.at(i);
address[] memory gaugeAddresses = gaugeRegistrar.getGaugesByRewardController(
    controller
);
```

Furthermore, execution will only revert in `UnifiedBudgetAllocator::allocateBudget` due to the total collected votes being zero if there are no valid registered gauges across any of the active controllers:

```solidity
// Calculate total votes across all controllers
uint256 totalVotes = 0;
for (uint256 i = 0; i < _voteTotals.length; i++) {
    totalVotes += _voteTotals[i];
}

// Revert if no votes to prevent division by zero
if (totalVotes == 0) revert ZeroTotalVotes();
```

Thus, if the DAO makes a mistake when calling `setModuleForController()` with a controller that is not already associated with gauge(s) registered on the `GaugeRegistrar`, distribution will be skipped and rewards will not be sent to the expected gauge.

**Recommended Mitigation:** Consider validating that the gauge addresses associated with a given controller are already registered on the `GaugeRegistrar`.

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
