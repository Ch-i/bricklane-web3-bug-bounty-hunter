---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-4
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
title: Budget is always calculated using the full `epochDuration` regardless of the
  actual timing of distributions
vuln_class: []
---

# Budget is always calculated using the full `epochDuration` regardless of the actual timing of distributions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The `DistributionManager` calculates budget allocations based on the full epoch duration and transfers tokens to reward controllers at the end of each epoch. When reward speeds are updated via calls to `setRewardSpeedInternal()`, the budget calculation assumes rewards will be distributed for the entire epoch duration; however, depending on the timing of distribution, this can result in a mismatch between the tokens transferred and tokens actually distributed as rewards.

```solidity
// BenqiCoreModule::calculateMarketBudgetUsed
function calculateMarketBudgetUsed(
    MarketVotes memory _market,
    uint256 _supplySpeed,
    uint256 _borrowSpeed,
    uint256 _epochDuration
) public pure returns (uint256) {
    uint256 budget = 0;

    // Only count budget for registered gauges
    if (_market.hasRegisteredSupplyGauge) {
@>      budget += _supplySpeed * _epochDuration; // @audit - uses full epoch duration
    }

    if (_market.hasRegisteredBorrowGauge) {
@>      budget += _borrowSpeed * _epochDuration; // @audit - uses full epoch duration
    }

    return budget;
}

// DistributionManager::_buildActions
uint256 amountWithBuffer = _applyBuffer(budgetUsed);
if (amountWithBuffer != 0) {
    actions[actionCount++] = Action({
        to: address(rewardToken),
        value: 0,
        data: abi.encodeWithSelector(
            IERC20.transfer.selector,
            controller,
@>          amountWithBuffer // @audit - full epoch budget transferred
        )
    });
}
```

When speeds are set in the Comptroller, rewards accrue from the instantaneous timestamp onwards while the previous speeds are overwritten and undistributed budget is not taken into consideration:

```solidity
    function setRewardSpeedInternal(uint8 rewardType, QiToken qiToken, uint newSupplyRewardSpeed, uint newBorrowRewardSpeed) internal {
        uint currentSupplyRewardSpeed = supplyRewardSpeeds[rewardType][address(qiToken)];
        uint currentBorrowRewardSpeed = borrowRewardSpeeds[rewardType][address(qiToken)];

        if (currentSupplyRewardSpeed != 0) {
@>          updateRewardSupplyIndex(rewardType, address(qiToken));
        } else if (newSupplyRewardSpeed != 0) {
            Market storage market = markets[address(qiToken)];
            require(market.isListed, "Market is not listed");

            ...
         }

        ...

        if (currentSupplyRewardSpeed != newSupplyRewardSpeed) {
@>          supplyRewardSpeeds[rewardType][address(qiToken)] = newSupplyRewardSpeed;
            emit SupplyRewardSpeedUpdated(rewardType, qiToken, newSupplyRewardSpeed);
        }

       ...
    }

    // lib/BENQI-Smart-Contracts/lending/Comptroller.sol:1112-1130
    function updateRewardSupplyIndex(uint8 rewardType, address qiToken) internal {
        require(rewardType <= 1, "rewardType is invalid");
        RewardMarketState storage supplyState = rewardSupplyState[rewardType][qiToken];
        uint supplySpeed = supplyRewardSpeeds[rewardType][qiToken];
        uint blockTimestamp = getBlockTimestamp();
@>      uint deltaTimestamps = sub_(blockTimestamp, uint(supplyState.timestamp)); // @audit - accrues from last update
        if (deltaTimestamps > 0 && supplySpeed > 0) {
            uint supplyTokens = QiToken(qiToken).totalSupply();
@>          uint qiAccrued = mul_(deltaTimestamps, supplySpeed); // @audit - deltaTimestamps < epochDuration
            Double memory ratio = supplyTokens > 0 ? fraction(qiAccrued, supplyTokens) : Double({mantissa: 0});
            Double memory index = add_(Double({mantissa: supplyState.index}), ratio);
            rewardSupplyState[rewardType][qiToken] = RewardMarketState({
                index: safe224(index.mantissa, "new index exceeds 224 bits"),
                timestamp: safe32(blockTimestamp, "block timestamp exceeds 32 bits")
            });
        } else if (deltaTimestamps > 0) {
            supplyState.timestamp = safe32(blockTimestamp, "block timestamp exceeds 32 bits");
        }
    }
```

Taking in consideration the fact that there is also an additional buffer amount that is transferred to the reward controller and that this discrepancy can occur on every epoch, these non-negligible losses will accumulate over time.

It is understood that there can be no retroactive distributions in the event of delays, and the addition of a voting buffer is added to account for potential delays based on the fact that, while operators are assumed to trigger distributions at roughly the same interval, this is not currently fully automated and thus not guaranteed. However, it is still not clear when exactly the operators are expected to execute distribution at roughly the same time every epoch strictly before the epoch ends. If so, this means that a portion of the budget will always be wasted, exacerbated by the addition of the buffer amount.

This is unavoidable unless perhaps distributions can occur after the end of the epoch, e.g. in the hour window before voting starts again in the next epoch, in which case the operators should optimally target strictly the end of the epoch or later. Unfortunately, as documented separately, this is not possible based on the current logic as an attempted distribution during this period would incorrectly mark the next distribution as complete even when voting has not yet started. Ideally, this logic would be modified to support distributions for epoch N during the initial buffer period of epoch N+1.

**Impact:** Depending on when `distribute()` is called, a part of the transferred budget may never be distributed.

**Proof of Concept:** Consider the following example:

* Day 0-7: Voting active
* Day 7: Voting ends
* Day 10: `distribute()` is called (3 days after voting ends)
    * Budget calculated: speed * 2 weeks = 1000 tokens
    * Tokens transferred to Comptroller: 1000 tokens (not counting extra buffer)
    * New speed set: 500 tokens/week (71.43 tokens/day)
* Day 10-14: Rewards accrue at 71.43 tokens/day = ~286 tokens
* Day 14: Epoch N ends (but speed continues unchanged)
* Day 14-21 (Epoch N+1): Voting active, rewards STILL accrue at 71.43 tokens/day = ~500 tokens
* Day 21: Voting ends
* Day 22: Next `distribute()` is called

* Total time at old speed: Day 10 to Day 22 = 12 days
* Total distributed from Epoch N budget: 71.43 * 12 = ~857 tokens
* Wasted from Epoch N: 1000 - 857 = ~143 tokens

The following test should be added to `DistributeManager.distribute.t,sol`:

```solidity
function test_wastedBudgetPoC() public {
    // Setup two gauges
    vm.startPrank(ADMIN);
    address gauge1 = gaugeRegistrar.registerGauge(
        QI_TOKEN_1, IGaugeRegistrar.Incentive.Supply, address(coreComptroller), "Gauge 1"
    );
    address gauge2 = gaugeRegistrar.registerGauge(
        QI_TOKEN_2, IGaugeRegistrar.Incentive.Supply, address(coreComptroller), "Gauge 2"
    );
    vm.stopPrank();

    coreComptroller.setMarketListed(QI_TOKEN_1, true);
    coreComptroller.setMarketListed(QI_TOKEN_2, true);

    // Epoch 0: gauge1 gets 80% of votes, gauge2 gets 20%
    addressGaugeVoter.setEpochGaugeVotes(0, gauge1, 800 ether);
    addressGaugeVoter.setEpochGaugeVotes(0, gauge2, 200 ether);

    // Epoch 0: Voting ends Day 7, distribute() called Day 10 (3 day delay)
    uint256 distributeDay10 = 1 weeks + 3 days;
    vm.warp(distributeDay10);

    vm.prank(DISTRIBUTOR);
    distributionManager.distribute();

    uint256 gauge1FirstSpeed = coreComptroller.supplyRewardSpeeds(0, QI_TOKEN_1);

    // Epoch 1: Votes SHIFT - gauge1 now only gets 30%, gauge2 gets 70%
    addressGaugeVoter.setEpochGaugeVotes(0, gauge1, 300 ether);
    addressGaugeVoter.setEpochGaugeVotes(0, gauge2, 700 ether);

    uint256 distributeDay22 = 2 weeks + 1 weeks + 1 days;
    vm.warp(distributeDay22);

    vm.prank(DISTRIBUTOR);
    distributionManager.distribute(); // Overwrites speeds from Epoch 0

    // Check: gauge1 speed REDUCED (now only 30% of budget)
    uint256 gauge1NewSpeed = coreComptroller.supplyRewardSpeeds(0, QI_TOKEN_1);

    assertGt(gauge1FirstSpeed, gauge1NewSpeed, "Speed REDUCED when votes decreased and budget wasted!");
}
```

**Recommended Mitigation:** Distributions for epoch N would ideally be made during the initial buffer period of epoch N+1.

The integration tests notably do not cover distributions beyond the expected token transfers to the distributor rather than also testing claims by market participants. To effectively demonstrate the scenario described above, an assertion should be implemented for the claimable vs transferred amount.

**BENQI:** We acknowledge that the nature of the distributor means that, indeed some funds in the contracts may go unclaimed due to the buffer.

We also note that each rewards controller implementation defines sweep/rescue functions for the admin to recover funds if they require it. These are `_grantQi` and `_rescueFunds` for the comptroller and distributor respectively.

Our idea was that a small excess is preferable to running short, as funds can be asynchronously retrieved without affecting users, while the reverse is not true.

We also note that the admins are freely able to reduce the buffer, in order to reduce the excess.

**Cyfrin:** Acknowledged.
