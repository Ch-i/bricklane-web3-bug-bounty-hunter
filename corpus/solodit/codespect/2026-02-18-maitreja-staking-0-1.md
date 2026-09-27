---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-18-maitreja-staking-0-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md
tags:
- firm:codespect
- report:2026-02-18-maitreja-staking
title: '[L-02] Withdrawal request does not prevent rewards from accrual'
vuln_class: []
---

# [L-02] Withdrawal request does not prevent rewards from accrual

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-18-Maitreja-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md)_

---

**Files:** [ProgressiveStaking.sol](https://github.com/whaleden-mjtd/maitme-contracts-staking/blob/ce61102843ceb1c27d875b394490ff859577016c/src/ProgressiveStaking.sol#L240)

**Description:**

The `ProgressiveStaking` contracts provides a two-step withdrawal process where the staker first needs to call `requestWithdraw(...)`, then `executeWithdraw(...)`. where the `executeWithdraw(...)` can be called after `NOTICE_PERIOD` passes. The problem is that there is no effect on the stake after calling `requestWithdraw(...)`, so a user could call it immediately after creating a stake and then wait just until he wants to unstake and call `executeWithdraw(...)`, which in practical terms mean that the `NOTICE_PERIOD` can be ignored as longs the user calls `requestWithdraw(...)` early.

**Impact:** Practical lack of expected notice period for withdrawing the stake.

**Recommendation:** The `requestWithdraw(...)` function should stop accrual of the rewards.

**Status:** Fixed
