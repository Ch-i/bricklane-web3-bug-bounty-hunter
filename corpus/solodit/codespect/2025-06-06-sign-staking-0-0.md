---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-06-sign-staking-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-06-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md
tags:
- firm:codespect
- report:2025-06-06-sign-staking
title: '[H-01] Interest not claimable after unstaking whole stake'
vuln_class: []
---

# [H-01] Interest not claimable after unstaking whole stake

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-06-SIGN-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md)_

---

**Files:** [SIGNStaking.sol](https://github.com/EthSign/sign-token-staking-evm/blob/735cc008ea45c4a54e87761217218fb3983e69d5/src/SIGNStaking.sol#L319)

**Description:**

The `claimInterest(...)` function allows the staker to claim interest. This function was added to decouple claiming the interest from unstaking.

`claimInterest(...)` when called updates the interest according to the latest timestamp:

```solidity
_updateInterest(msg.sender);
```

The `_updateInterest(...)` uses `calculateInterest(...)` to return the latest accrued interest and assigns the value to `userStake.accumulatedInterest`.

The issue happens when the user first unstakes his or her entire stake, but does not collect interest before. After user empties the stake the `userStake.principalAmount` is set to `0`. This causes the following condition to be hit inside the `calculateInterest(...)`:

```solidity
if (userStake.principalAmount == 0) {
    return 0;
}
```

Which means that the user’s `userStake.accumulatedInterest` will also be set to zero. This will cause the following line at `claimInterest(...)` to revert:

```solidity
userStake.accumulatedInterest -= amount;
```

The user will be unable to claim interest, the only way to recover from this is to call `stake(...)` again, but that will reset the `userStake.accumulatedInterest` back to `0`.

**Impact:** Loss of accrued interest when claiming after unstaking. The possibility of such a scenario is high, hence the High impact of this issue.

**Recommendation:** Change the `calculateInterest(...)` return value from `0` to `userStake.accumulatedInterest` when `userStake.principalAmount` is `0`.

**Status:** Fixed

**Update from TokenTable:** [f5c92216ffad8b1e875f2e5cde63c7932a399354](https://github.com/EthSign/sign-token-staking-evm/commit/f5c92216ffad8b1e875f2e5cde63c7932a399354)
