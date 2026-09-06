---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Asymmetric gauge unregistration can result in misallocation of tokens
vuln_class: []
---

# Asymmetric gauge unregistration can result in misallocation of tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The reward speed preservation logic in the `BenqiCoreModule` contract enables indefinite QI token distributions for markets associated with asymmetrically unregistered or otherwise expired supply/borrow gauges. Specifically, when a gauge is unregistered via `GaugeRegistrar::unregisterGauge`, it is removed from the internal tracking sets `_allGauges` and `_gaugesByRewardController` before being deactivated in the linked `AddressGaugeVoter`, preventing future votes. However, in `BenqiCoreModule::generateActions`, the `calculateSpeeds()` function checks the `hasRegisteredSupplyGauge` and `hasRegisteredBorrowGauge` flags. If a flag is false, the existing supply or borrow reward speed from `CoreComptroller` is preserved rather than being set to zero. This intentional design avoids abrupt changes to reward speed but lacks an automatic zeroing mechanism, allowing speeds to persist at their last non-zero value unless governance manually intervenes with a direct call to `setRewardSpeed()`.

**Impact:** Markets with asymmetrically unregistered gauges can continue distributing QI rewards indefinitely, leading to misallocation of tokens outside the system's budgeted epochs. This could exhaust QI reward pools over time or necessitate unplanned replenishments. The economic loss scales with market activity (e.g., supply/borrow volumes triggering claims), preserved speed levels, and duration before detection. It introduces an operational risk reliant on vigilant governance; if unregistration occurs without follow-up (e.g., due to oversight in a DAO process), it may result in significant, cumulative token leakage, though this is not directly exploitable by external actors.

**Proof of Concept:** The following test should be added to `BenqiCoreModule.generateActions.t.sol`:

```solidity
function test_deactivateSupplyGauge_usesExistingSpeed() public {
    // Set existing speeds
    comptroller.setRewardSpeeds(QITOKEN_1, 1000, 2000);

    // Only provide borrow gauge, not supply
    IDistributionGaugeVote.GaugeVote[] memory gauges = new IDistributionGaugeVote.GaugeVote[](1);
    gauges[0] = IDistributionGaugeVote.GaugeVote({
    	gaugeAddress: GAUGE_1,
    	qiToken: QITOKEN_1,
    	incentive: IGaugeRegistrar.Incentive.Borrow,
    	votes: 100
    });

    (Action[] memory actions, ) = module.generateActions(
    	address(comptroller),
    	gauges,
    	MODULE_BUDGET,
    	EPOCH_DURATION
    );

    // Decode the action to check speeds
    (, , uint256 supplySpeed, uint256 borrowSpeed) = decodeSetRewardSpeed(actions[0].data);

    // Borrow speed should be calculated from votes
    uint256 expectedBorrowSpeed = ((MODULE_BUDGET / EPOCH_DURATION) * 100) / 100;
    assertEq(borrowSpeed, expectedBorrowSpeed);
    assertGt(borrowSpeed, 0);
    assertNotEq(borrowSpeed, 2000);

    // Supply speed should be preserved
    assertEq(supplySpeed, 1000);
}
```

**Recommended Mitigation:** Consider removing the speed preservation logic. This could be achieved by modifying `BenqiCoreModule::calculateSpeeds` to always recalculate speeds for all gauges based on current votes, setting them to zero or `MIN_SPEED` when `hasRegisteredSupplyGauge` or `hasRegisteredBorrowGauge` is false, rather than preserving the current comptroller speeds.

**BENQI:** This turned out to be a bigger PR than anticipated. We first implemented the unregistration hook via a pattern of:

Registrar calls Distribution Manager via a dedicated endpointed auth’d to the Registrar. The Distribution Manager queries the associated module to get the unregister actions. The Distribution manager executes as it has the permission on the DAO for the speed adjustments.

This created a problem though: gauges could be registered without a check to see if they actually existed. This meant gauges could be registered but could not be unregistered and this would permanently block distribution as, in both cases, we would attempt to read from a nonlisted gauge.

We therefore added 2 safety measures:

1. A check to see the gauge exists, during registration. This should cover 95% of cases.
2. A try/catch with a dedicated event emitted if unregistration fails. This would necessitate further action from the admin to understand the issue but is the same as the base case.

Fixed in PR [\#24](https://github.com/aragon/benqi-governance/pull/24).

**Cyfrin:** Verified. Unregistration of a valid gauge first updates the current speed on the `Comptroller` to the `MIN_SPEED` in the unregister actions such that future allocations are minimized.
