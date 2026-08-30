---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: A malicious staker can delay the increase of any delegator's voteWeight as
  much as he wants
vuln_class: []
---

# A malicious staker can delay the increase of any delegator's voteWeight as much as he wants

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** When a staker delegates his balance to a delegator, the time duration variable `_weights[delegate].stakeTime` is decreased. However, when undelegating only the balance is decreased. This makes it possible a malicious user can decrease `_weights[delegate].stakeTime`. He can expand the impact of this attack by repeating delegating and undelegating.

**Impact:** A malicious user can delay the increase of any delegator's `voteWeight` as much as he wants.

**Proof of Concept:** Here's an example scenario:

Assume that `HalfTime` is `7`days.
1. Alice delegates `200` to Bob(a victim).
2. `14` days passed. `t` is `14`.
                       Bob's `votePower` is `200*14/(14+7)=133`.
4. Charlie(a malicious user) delegates `100` to Bob. `t` decreases from `14` to `200*14*7/(300*(14+7)-200*14)=5.6`
                       Bob's `votePower` is `300*5.6/(5.6+7)=133`.
5. Charlie undelegates `100` from Bob. `t` is still `5.6`. However, `balance` is decreased from `300` to `200`.
                       Bob's `votePower` is `200*5.6/(5.6+7)=88`.

A malicious user can decrease the `t` as much as he wants by repeating step 3 and 4 in one transaction.
In this way, he can delay the increase of `votePower` as much as he wants. In the worst case, it is possible to limit the `votePower` of any user almost 0 forever.

Note: Two combining ways of delegation (step 3) and undelegation (step 4) are possible.
One is the combination of `setUserVoteDelegate()` and `unsetUserVoteDelegate()`.
Another is the combination of `stake()` and `withdraw()`.

**Recommended Mitigation:** The mechanism for adjusting the stakingTime between delegation and undelegation should be improved.

**TempleDAO:** Fixed in [PR 1041](https://github.com/TempleDAO/temple/pull/1041)

**Cyfrin:** Verified
