---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Function `getTotalStake()` fails to account for pending validators, leading
  to inaccurate accounting
vuln_class: []
---

# Function `getTotalStake()` fails to account for pending validators, leading to inaccurate accounting

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** The `getTotalStake()` function is the core accounting function to calculate the total stake of the `CasimirManager`. It's used to compute the change for `rewardStakeRatioSum` within the `finalizeReport()` function.

```solidity
function getTotalStake() public view returns (uint256 totalStake) {
  // @audit Validators in pending state is not accounted for
  totalStake = unassignedBalance + readyValidatorIds.length * VALIDATOR_CAPACITY + latestActiveBalanceAfterFee
      + delayedEffectiveBalance + withdrawnEffectiveBalance + subtractRewardFee(delayedRewards) - unstakeQueueAmount;
}
```

This function aggregates the stakes from various sources, including the `32 ETH` from each "ready validator" (`readyValidatorIds.length * VALIDATOR_CAPACITY`) and the ETH staked in "staked validators" (`latestActiveBalanceAfterFee`).

However, it fails to account for the ETH in pending validators.

A validator must go through three steps to become active/staked:

1. Every time users make a deposit, the contract checks if the unassigned balance has reached `32 ETH`. If it has, the next validator ID is added to `readyValidatorIds`.
2. The reporter calls `depositValidator()` to deposit `32 ETH` from the validator into the beacon deposit contract. In this step, the validator ID moves from `readyValidatorIds` to `pendingValidatorIds`.
3. The reporter calls `activateValidator()`, which moves the validator ID from `pendingValidatorIds` to `stakedValidatorIds` and updates `latestActiveBalanceAfterFee` to reflect the total stake in the beacon chain.

As shown, the `getTotalStake()` function accounts for validators in steps 1 and 3, but ignores the stake of validators in the pending state (step 2). In the current design, there is nothing that stops report finalization if pending validators > 0.

**Impact:** Function getTotalStake() will return the value of total stake less than it should be. The result is rewardStakeRatioSum calculation will be incorrect in a scenario where all pending validators are not activated before report finalization.

```solidity
uint256 totalStake = getTotalStake();

rewardStakeRatioSum += Math.mulDiv(rewardStakeRatioSum, gainAfterFee, totalStake);

rewardStakeRatioSum += Math.mulDiv(rewardStakeRatioSum, gain, totalStake);

rewardStakeRatioSum -= Math.mulDiv(rewardStakeRatioSum, loss, totalStake);
```

**Recommended Mitigation:** Consider adding `pendingValidatorIds.length * VALIDATOR_CAPACITY` to function `getTotalStake()`.

**Casimir:**
Fixed in [10fe228](https://github.com/casimirlabs/casimir-contracts/commit/10fe228406dc3f889db42e8850add94561a7325e)

**Cyfrin:** Verified.
