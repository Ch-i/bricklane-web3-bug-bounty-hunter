---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-2
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
title: Delayed rewards can be claimed without updating internal accounting
vuln_class: []
---

# Delayed rewards can be claimed without updating internal accounting

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** The `claimRewards()` function is designed to claim delayed withdrawals from the EigenLayer Delayed Withdrawal Router and to update accounting variables such as `delayedRewards` and `reservedFeeBalance`.

```solidity
function claimRewards() external {
    onlyReporter();

    uint256 initialWithdrawalsBalance = address(eigenWithdrawals).balance;
    eigenWithdrawals.claimDelayedWithdrawals(
        eigenWithdrawals.getClaimableUserDelayedWithdrawals(address(this)).length
    );
    uint256 claimedAmount = initialWithdrawalsBalance - address(eigenWithdrawals).balance;
    delayedRewards -= claimedAmount;

    uint256 rewardsAfterFee = subtractRewardFee(claimedAmount);
    reservedFeeBalance += claimedAmount - rewardsAfterFee;
    distributeStake(rewardsAfterFee);

    emit RewardsClaimed(rewardsAfterFee);
}
```

However, this function can be bypassed by directly executing the claim on the EigenLayer side via the `DelayedWithdrawalRouter::claimDelayedWithdrawals()` function. This function allows the caller to claim withdrawals for a specified recipient, with the recipient's address provided as an input. If the `CasimirManager` contract address is used as the `recipient`, the claim is made on its behalf.

**Impact:** This process does not update the accounting variables, leading to inaccurate accounting within the contract. Even though the rewards have been claimed, they are still accounted for in the `delayedRewards`, resulting in an incorrect total stake value.

**Proof of Concept:** EigenLayer contract that handles delayed withdrawal claims can be found [here](https://github.com/Layr-Labs/eigenlayer-contracts/blob/0139d6213927c0a7812578899ddd3dda58051928/src/contracts/pods/DelayedWithdrawalRouter.sol#L80)

**Recommended Mitigation:** Consider altering the way the contract manages rewards claims. This could be achieved by moving the accounting for claimed reward amounts to the `receive()` function, and by only filtering funds received from the `eigenWithdrawals` contract.

**Casimir:**
Fixed in [4adef64](https://github.com/casimirlabs/casimir-contracts/commit/4adef6482238c3d0926f72ffdff04e7a49886045)

**Cyfrin:** Verified.
