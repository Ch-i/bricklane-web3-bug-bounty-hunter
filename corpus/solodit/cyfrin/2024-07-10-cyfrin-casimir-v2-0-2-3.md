---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Function `withdrawRewards()` may lead to inaccuracy in `delayedRewards` if
  there's no withdrawal to process
vuln_class: []
---

# Function `withdrawRewards()` may lead to inaccuracy in `delayedRewards` if there's no withdrawal to process

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** In the `CasimirManager`, the `withdrawRewards()` function can be used by the reporter to process swept validator rewards. The reporter must provide `WithdrawalProofs`, which the function uses to call `eigenPod.verifyAndProcessWithdrawals()`.
```solidity
function withdrawRewards(WithdrawalProofs memory proofs) external {
    onlyReporter();

    eigenPod.verifyAndProcessWithdrawals(
        proofs.oracleTimestamp,
        proofs.stateRootProof,
        proofs.withdrawalProofs,
        proofs.validatorFieldsProofs,
        proofs.validatorFields,
        proofs.withdrawalFields
    );

    // @audit Not check if the delayed withdrawal length has changed or not
    uint256 delayedAmount = eigenWithdrawals.userDelayedWithdrawalByIndex(
        address(this), eigenWithdrawals.userWithdrawalsLength(address(this)) - 1
    ).amount;
    delayedRewards += delayedAmount;

    emit RewardsDelayed(delayedAmount);
}
```

The `verifyAndProcessWithdrawals()` function processes a list of withdrawals and sends them as one withdrawal to the delayed withdrawal router. However, it only creates a new withdrawal in the delayed router if the sum of the amount to send is non-zero.

```solidity
if (withdrawalSummary.amountToSendGwei != 0) {
    _sendETH_AsDelayedWithdrawal(podOwner, withdrawalSummary.amountToSendGwei * GWEI_TO_WEI);
}
```

So, if the reporter calls `withdrawRewards()` with no withdrawals, i.e., empty `withdrawalFields` and `validatorFields`, the delayed withdrawal router will not create a new entry. However, as `withdrawRewards()` always takes `delayedAmount` as the latest entry from the delayed withdrawal router, it actually retrieves an old amount that has already been accounted for.

**Impact:** If the reporter mistakenly calls `withdrawRewards()` with no withdrawals, `delayedRewards` will account for the previous delayed amount again, leading to incorrect accounting.

**Recommended Mitigation:** Consider following the pattern in the `withdrawValidator()` function. It checks if the length of `eigenWithdrawals.userWithdrawalsLength()` changes before adding the amount to `delayedRewards`.
```solidity
uint256 initialDelayedRewardsLength = eigenWithdrawals.userWithdrawalsLength(address(this));
uint64 initialDelayedEffectiveBalanceGwei = eigenPod.withdrawableRestakedExecutionLayerGwei();

eigenPod.verifyAndProcessWithdrawals(
    ...
);

{
    uint256 updatedDelayedRewardsLength = eigenWithdrawals.userWithdrawalsLength(address(this));
    if (updatedDelayedRewardsLength > initialDelayedRewardsLength) {
        IDelayedWithdrawalRouter.DelayedWithdrawal memory withdrawal =
            eigenWithdrawals.userDelayedWithdrawalByIndex(address(this), updatedDelayedRewardsLength - 1);
        if (withdrawal.blockCreated == block.number) {
            delayedRewards += withdrawal.amount;

            emit RewardsDelayed(withdrawal.amount);
        }
    }
}
```

**Casimir:**
Fixed in [81cb7f1](https://github.com/casimirlabs/casimir-contracts/commit/81cb7f19aaa0dfad5101bcfa8a233fe0fade9365)

**Cyfrin:** Verified.
