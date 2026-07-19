---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Inefficient rewards collection pattern in the `PolygonStrategy::unbond()` function
  leads to unnecessary gas consumption
vuln_class: []
---

# Inefficient rewards collection pattern in the `PolygonStrategy::unbond()` function leads to unnecessary gas consumption

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** The current implementation of the `PolygonStrategy::unbond()` function processes vaults sequentially and makes immediate unbonding decisions on a per-vault basis.

This approach can lead to unnecessary unbonding operations when the total rewards across all vaults would be sufficient to cover the withdrawal amount.

In the current implementation:

1. The function iterates through each vault
2. For each vault, it extracts rewards if available
3. If rewards from a single vault are insufficient, it immediately unbonds principal from that vault
4. It continues this process until the full `_toUnbond` amount is satisfied

This implementation doesn't consider the total available rewards across all vaults before making unbonding decisions, resulting in potential unnecessary unbonding operations that consume significant gas.

**Impact:**
- Higher gas costs: Each unnecessary unbonding operation consumes additional gas, especially since it later requires a separate unstakeClaim call to finalize the withdrawal

- Capital inefficiency: Unbonding principal when rewards would have been sufficient reduces the amount of capital earning yields in the protocol

- Longer waiting periods: Unlike rewards, unbonded principal is subject to waiting periods before it can be re-used or withdrawn

**Recommended Mitigation:** Refactor the unbond() function to use a two-phase approach:
1. Collect all rewards until the cumulative rewards are enough to honor unbonding request
2. Start vault unbonding only after all rewards are collected.

Here is a sample implementation:

```solidity
function unbond(uint256 _toUnbond) external onlyFundFlowController {
    if (numVaultsUnbonding != 0) revert UnbondingInProgress();
    if (_toUnbond == 0) revert InvalidAmount();

    uint256 toUnbondRemaining = _toUnbond;
    uint256 preBalance = token.balanceOf(address(this));
    uint256 skipIndex = validatorRemoval.isActive ? validatorRemoval.validatorId : type(uint256).max;
    uint256 numVaultsUnbonded;

    // @audit Phase 1 -> Withdraw all rewards first
    for (uint256 i = 0; i < vaults.length; i++) {
        if (i != skipIndex) {
            IPolygonVault vault = vaults[i];
            uint256 rewards = vault.getRewards();

            if (rewards > 0) {
                vault.withdrawRewards();

                // @audit Check if we've collected enough rewards
                uint256 currentBalance = token.balanceOf(address(this));
                uint256 collectedRewards = currentBalance - preBalance;
                if (collectedRewards >= toUnbondRemaining) {
                    // @audit We've collected enough rewards, no need to unbond principal
                    totalQueued += collectedRewards;
                    emit Unbond(_toUnbond);
                    return;
                }
            }
        }
    }

    // @audit Phase 2: If rewards weren't enough, unbond principal
    uint256 rewardsCollected = token.balanceOf(address(this)) - preBalance;
    toUnbondRemaining -= rewardsCollected;

    uint256 i = validatorWithdrawalIndex;
    while (toUnbondRemaining != 0) {
        if (i != skipIndex) {
            IPolygonVault vault = vaults[i];
            uint256 principalDeposits = vault.getPrincipalDeposits();

            if (principalDeposits != 0) {
                uint256 vaultToUnbond = principalDeposits >= toUnbondRemaining
                    ? toUnbondRemaining
                    : principalDeposits;

                vault.unbond(vaultToUnbond);
                toUnbondRemaining -= vaultToUnbond;
                ++numVaultsUnbonded;
            }
        }

        ++i;
        if (i >= vaults.length) i = 0;
    }

    validatorWithdrawalIndex = i;
    numVaultsUnbonding = numVaultsUnbonded;
    totalQueued += token.balanceOf(address(this)) - preBalance;

    emit Unbond(_toUnbond);
}
```

**Stake.Link:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
