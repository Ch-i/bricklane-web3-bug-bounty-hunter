---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-4
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
title: Front-run withdrawValidator by submitting proofs can permanently DOS validator
  unstaking on EigenLayer
vuln_class: []
---

# Front-run withdrawValidator by submitting proofs can permanently DOS validator unstaking on EigenLayer

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** An attacker can observe the mempool and front-run the `CasimirManager::withdrawValidator` transaction by submitting the same proofs directly on Eigen Layer.

Since the proof is already verified, the `CasimirManager::withdrawValidator` transaction will revert when it tries to submit the same proofs. Submitting an empty proof to bypass proof verification also does not work because the `finalEffectiveBalance` will always be 0, preventing the queuing of withdrawals.

````solidity
function withdrawValidator(
    uint256 stakedValidatorIndex,
    WithdrawalProofs memory proofs,
    ISSVClusters.Cluster memory cluster
) external {
    onlyReporter();

   // ..code...

    uint256 initialDelayedRewardsLength = eigenWithdrawals.userWithdrawalsLength(address(this)); //@note this holds the rewards
    uint64 initialDelayedEffectiveBalanceGwei = eigenPod.withdrawableRestakedExecutionLayerGwei(); //@note this has the current ETH balance

>   eigenPod.verifyAndProcessWithdrawals(
        proofs.oracleTimestamp,
        proofs.stateRootProof,
        proofs.withdrawalProofs,
        proofs.validatorFieldsProofs,
        proofs.validatorFields,
        proofs.withdrawalFields
    ); //@audit reverts if proof is already verified

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

    uint64 updatedDelayedEffectiveBalanceGwei = eigenPod.withdrawableRestakedExecutionLayerGwei();
>   uint256 finalEffectiveBalance =
        (updatedDelayedEffectiveBalanceGwei - initialDelayedEffectiveBalanceGwei) * GWEI_TO_WEI; //@audit if no proofs submitted, this will be 0
    delayedEffectiveBalance += finalEffectiveBalance;
    reportWithdrawnEffectiveBalance += finalEffectiveBalance;
}

//... code
````

**Impact:** At a negligible cost, an attacker can prevent validator withdrawals on EigenLayer, creating an insolvency risk for Casimir.

**Recommended Mitigation:** Consider making the following changes to `CasimirManager::withdrawValidators`:

- Split the function into two separate functions, one for full-withdrawal verifications and another for queuing verified withdrawals.
- Listen to the following event emission in `EigenPod::_processFullWithdrawal` and filter the events emitted with the recipient as `CasimirManager`.
````solidity
event FullWithdrawalRedeemed(
    uint40 validatorIndex,
    uint64 withdrawalTimestamp,
    address indexed recipient,
    uint64 withdrawalAmountGwei
);
````
- Introduce a try-catch while verifying withdrawal for each applicable validator index. If a proof is already verified, update the `stakedValidatorIds` array and reduce `requestedExits` in the catch section.
- Once all withdrawals are verified, use the event emissions to create a `QueuedWithdrawalParams` array that will be sent to the second function that internally calls `eigenDelegationManager.queueWithdrawals(params)`.
- Update the `delayedEffectiveBalance` and `reportWithdrawnEffectiveBalance` at this stage.

Note: This assumes that the `reporter` is protocol-controlled.

**Casimir:**
Fixed in [eb31b43](https://github.com/casimirlabs/casimir-contracts/commit/eb31b4349e69eb401615e0eca253e9ab8cc0999d)

**Cyfrin:** Verified. Withdrawal proofs are decoupled from queuing withdrawals on EigenLayer. This successfully mitigates the Denial of Service risk reported in this issue. It is noted however that the effective balance is hardcoded as 32 ether.

It is recommended that the effective balance is passed as a parameter by monitoring the full withdrawal event on EigenLayer.
