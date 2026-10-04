---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-18-maitreja-staking-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md
tags:
- firm:codespect
- report:2026-02-18-maitreja-staking
title: '[I-02] The MIN_STAKE_AMOUNT check is not applied during withdrawal requests'
vuln_class: []
---

# [I-02] The MIN_STAKE_AMOUNT check is not applied during withdrawal requests

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-18-Maitreja-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md)_

---

**Files:** [ProgressiveStaking.sol](https://github.com/whaleden-mjtd/maitme-contracts-staking/blob/ce61102843ceb1c27d875b394490ff859577016c/src/ProgressiveStaking.sol#L240)

**Description:**

In the `stake(...)` function, there is a position size check that requires the stake amount to be greater than `MIN_STAKE_AMOUNT`.

```solidity
function stake(uint256 amount) external nonReentrant whenNotPaused {
    if (amount == 0) revert ZeroAmount();
    if (amount < MIN_STAKE_AMOUNT) revert StakeAmountTooLow();
    //...
}
```

However, in the `requestWithdraw(...)` function, there is no check to ensure that the remaining position size after withdrawal is still greater than `MIN_STAKE_AMOUNT`. This may result in positions smaller than `MIN_STAKE_AMOUNT` existing in the contract.

**Impact:** Unexpected small positions may appear in the contract, which is unfavorable for management.

**Recommendation:** It is recommended to add a check in `requestWithdraw(...)`. If the remaining position size is not 0, it must be greater than `MIN_STAKE_AMOUNT`.

**Status:** Fixed
