---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-18-maitreja-staking-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md
tags:
- firm:codespect
- report:2026-02-18-maitreja-staking
title: '[L-01] Withdraw execution leads to lost rewards if not enough assets held
  by treasury'
vuln_class: []
---

# [L-01] Withdraw execution leads to lost rewards if not enough assets held by treasury

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-18-Maitreja-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md)_

---

**Files:** [ProgressiveStaking.sol](https://github.com/whaleden-mjtd/maitme-contracts-staking/blob/ce61102843ceb1c27d875b394490ff859577016c/src/ProgressiveStaking.sol#L304)

**Description:**

The `executeWithdraw(...)` function allows the holder of a stake to execute assets withdrawal. Inside the functions the rewards are calculated for the stake and are sent to the owner on condition that there is enough reward asset held at the contract:

```solidity
if (rewards > 0 && treasuryBalance >= rewards) {
    treasuryBalance -= rewards;
    stakingToken.safeTransfer(msg.sender, rewards);
    emit RewardsClaimed(msg.sender, stakeId, rewards, block.timestamp);
}
```

While this is done according to the protocol’s design, the issue is that if the withdrawal is partial and the `treasuryBalance` is insufficient the function still updates the `lastClaimTime`:

```solidity
position.lastClaimTime = block.timestamp;
```

which means that the rewards for the remaining amount are also lost.

**Impact:** Loss of rewards for the remainder of the stake.

**Recommendation:** It is recommended to only update the `lastClaimTime` when the rewards are actually successfully claimed. This way in case the `treasuryBalance` is insufficient, the stake owner will still be able to collect rewards later for the remainder of the stake once the treasury is replenished.

**Status:** Fixed
