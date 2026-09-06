---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[H-01] Users will forever lose their accrued rewards if they call `withdrawStake`
  before calling `claimReward` first'
vuln_class: []
---

# [H-01] Users will forever lose their accrued rewards if they call `withdrawStake` before calling `claimReward` first

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

**Impact:**
High, as this will lead to a monetary loss for users

**Likelihood:**
Medium, as even though the front-end will enforce the right sequence of calls, the Gitbook docs falsely claims re-staking will re-gain user's access to their rewards

**Description**

The contract is implemented so that if a user calls `withdrawStake` without first calling `claimReward` for each reward pool then the staker will lose all of his unclaimed rewards forever, they will be locked into the staking contract. While the front-end will enforce the right sequence of calls, the Gitbook docs state that `When un-staked, a user will lose access to all their pending rewards and lose access to future rewards (unless they re-stake)` which gives the impression that you can re-stake and then you will re-gain access to your unclaimed rewards, but this is not the case as the `withdrawStake` method removes the data needed for previous rewards calculation.

Since the docs give a misleading information about they way this mechanism works and also users can interact directly with the smart contract in a bad way for them (when they are not malicious) this has a higher likelihood of happening and resulting a monetary value loss for users.

**Recommendations**

One possible solution is to enforce zero unclaimed rewards when a call to `withdrawStake` is made by reverting if there are any such unclaimed rewards. Another one is to just call `claimReward` in `withdrawStake`.
